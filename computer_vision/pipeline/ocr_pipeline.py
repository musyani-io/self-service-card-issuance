import time
from typing import Dict, Optional

import cv2
import pytesseract

from core.card_detector import detect_card
from core.perspective_corrector import straighten_card
from core.anchor_roi import find_anchor_box, derive_rois_from_anchor
from core.image_utils import preprocess_for_ocr, resize_image
from core.student_id_validator import extract_student_id_robust
from core.exceptions import (
    CardNotFoundError,
    CardDetectionAmbiguousError,
    OCRExtractionError,
    PerspectiveCorrectionError,
    InvalidStudentIDError,
)


class CardOCRPipeline:
    def __init__(self, config: Dict):
        self.config = config

    def _log(self, message: str) -> None:
        if self.config.get("DEBUG", {}).get("verbose_logging", False):
            print(message)

    def scan_card(self, image) -> Dict:
        start = time.perf_counter()

        if image is None or getattr(image, "size", 0) == 0:
            return self._result(
                False,
                None,
                0.0,
                "input",
                "Invalid input image: None or empty",
                start,
            )

        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        max_width = self.config.get("MAX_INPUT_WIDTH")
        if max_width:
            try:
                image = resize_image(image, max_width=int(max_width))
            except Exception as e:
                return self._result(
                    False,
                    None,
                    0.0,
                    "preprocess",
                    f"Resize failed: {e}",
                    start,
                )

        try:
            corners = detect_card(image)
        except (CardNotFoundError, CardDetectionAmbiguousError) as e:
            return self._result(False, None, 0.0, "card_detection", str(e), start)

        if corners is None:
            return self._result(False, None, 0.0, "card_detection", "No card detected", start)

        try:
            straight = straighten_card(image, corners)
        except Exception as e:
            return self._result(
                False,
                None,
                0.0,
                "perspective",
                str(PerspectiveCorrectionError(str(e))),
                start,
            )

        anchor_box = find_anchor_box(
            straight,
            anchor_texts=self.config["ANCHOR_OCR"]["anchor_texts"],
            min_confidence=self.config["ANCHOR_OCR"]["min_confidence"],
            psm=self.config["ANCHOR_OCR"]["psm"],
            oem=self.config["ANCHOR_OCR"]["oem"],
            char_whitelist=self.config["ANCHOR_OCR"]["char_whitelist"],
        )

        if anchor_box is None:
            return self._result(False, None, 0.0, "anchor", "Anchor not found", start)

        derived = derive_rois_from_anchor(straight, anchor_box, self.config["ANCHOR_ROI_OFFSETS"])
        if "student_id" not in derived:
            return self._result(False, None, 0.0, "roi", "student_id ROI not found", start)

        student_roi = self._crop_roi_by_ratio(straight, derived["student_id"])
        pre = preprocess_for_ocr(student_roi, self.config.get("PREPROCESSING"))

        texts = self._run_ocr_strategies(pre)
        student_id = extract_student_id_robust(
            texts,
            self.config["STUDENT_ID_PATTERN"],
            self.config["VALID_YEAR_RANGE"],
            self.config["ID_TOTAL_LENGTH"],
        )

        if not student_id:
            return self._result(
                False,
                None,
                0.0,
                "ocr",
                str(InvalidStudentIDError("Student ID not found")),
                start,
            )

        return self._result(True, student_id, 1.0, "ocr", None, start)

    def _run_ocr_strategies(self, image) -> list[str]:
        configs = []
        base = self.config["TESSERACT_CONFIG_STRING"]
        configs.append(base)

        alt_psm = 7
        configs.append(
            f"--psm {alt_psm} --oem {self.config['TESSERACT_CONFIG']['oem']} "
            f"-c tessedit_char_whitelist={self.config['TESSERACT_CONFIG']['char_whitelist']}"
        )

        inv = cv2.bitwise_not(image)
        texts = []
        for cfg in configs:
            texts.append(pytesseract.image_to_string(image, config=cfg))
            texts.append(pytesseract.image_to_string(inv, config=cfg))

        return texts

    @staticmethod
    def _crop_roi_by_ratio(image, roi):
        h, w = image.shape[:2]
        x1 = int(roi["x_start"] * w)
        x2 = int(roi["x_end"] * w)
        y1 = int(roi["y_start"] * h)
        y2 = int(roi["y_end"] * h)
        return image[y1:y2, x1:x2]

    def _result(
        self,
        success: bool,
        student_id: Optional[str],
        confidence: float,
        method: str,
        error: Optional[str],
        start_time: float,
    ) -> Dict:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "success": success,
            "student_id": student_id,
            "confidence": confidence,
            "method": method,
            "error": error,
            "processing_time_ms": elapsed_ms,
        }
