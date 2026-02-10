import json
import sys
from pathlib import Path
import importlib.util

import cv2

# Resolve computer_vision root and load config directly from file
CV_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = CV_ROOT / "config" / "ocr_config.py"

if str(CV_ROOT) not in sys.path:
    sys.path.insert(0, str(CV_ROOT))

if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

spec = importlib.util.spec_from_file_location("ocr_config", CONFIG_PATH)
ocr_config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ocr_config)

from pipeline.ocr_pipeline import CardOCRPipeline

TEST_CARDS_DIR = CV_ROOT / "data" / "test_cards"
EXPECTED_RESULTS_PATH = CV_ROOT / "tests" / "expected_results.json"


def load_expected_results(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    expected = load_expected_results(EXPECTED_RESULTS_PATH)
    pipeline = CardOCRPipeline(ocr_config.__dict__)

    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]
    test_images = []
    for ext in image_extensions:
        test_images.extend(TEST_CARDS_DIR.glob(ext))

    test_images = sorted(test_images)
    if not test_images:
        print(f"No test images found in {TEST_CARDS_DIR}")
        return

    total = len(test_images)
    detected = 0
    extracted = 0
    correct = 0
    total_time = 0.0

    failures = []

    for image_path in test_images:
        image = cv2.imread(str(image_path))
        if image is None:
            failures.append(f"{image_path.name}: Failed to load image")
            continue

        result = pipeline.scan_card(image)
        total_time += result["processing_time_ms"]

        if result["success"]:
            detected += 1
            extracted += 1
        else:
            if result["method"] == "card_detection":
                failures.append(f"{image_path.name}: Card not detected")
            else:
                failures.append(f"{image_path.name}: OCR failed")

        expected_id = expected.get(image_path.name)
        if result["success"] and expected_id:
            if result["student_id"] == expected_id:
                correct += 1
            else:
                failures.append(
                    f"{image_path.name}: Wrong ID (expected: {expected_id}, got: {result['student_id']})"
                )

    detection_rate = (detected / total) * 100
    extraction_rate = (extracted / total) * 100
    accuracy_rate = (correct / total) * 100 if total else 0
    avg_time = total_time / total if total else 0

    print("===== OCR Pipeline Test Report =====")
    print(f"Total Images Tested: {total}")
    print(f"Cards Detected: {detected} ({detection_rate:.2f}%)")
    print(f"IDs Extracted: {extracted} ({extraction_rate:.2f}%)")
    print(f"Correct Extractions: {correct} ({accuracy_rate:.2f}%)")
    print(f"Overall Success Rate: {accuracy_rate:.2f}%")
    print(f"Average Time: {avg_time:.2f} ms")

    if failures:
        print("\nFailed Cases:")
        for item in failures:
            print(f"- {item}")


if __name__ == "__main__":
    main()
