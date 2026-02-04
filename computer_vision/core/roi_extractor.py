"""
ROI (Region of Interest) extraction for OCR.

Uses percentage-based coordinates defined in config/ocr_config.py
on the straightened card image.
"""

from typing import Dict
import numpy as np


def _clamp(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(value, max_value))


def extract_roi(card_image: np.ndarray, roi_config: Dict) -> Dict[str, np.ndarray]:
    """
    Extract regions of interest from a straightened card image.

    Args:
        card_image: Straightened card image (BGR)
        roi_config: Dictionary mapping region name to ROI ratios

    Returns:
        Dictionary mapping region name to cropped ROI image
    """
    if card_image is None or card_image.size == 0:
        raise ValueError("Invalid card image for ROI extraction")

    h, w = card_image.shape[:2]
    rois = {}

    for name, roi in roi_config.items():
        x_start = int(roi['x_start'] * w)
        x_end = int(roi['x_end'] * w)
        y_start = int(roi['y_start'] * h)
        y_end = int(roi['y_end'] * h)

        # Clamp to valid bounds
        x_start = _clamp(x_start, 0, w - 1)
        x_end = _clamp(x_end, 1, w)
        y_start = _clamp(y_start, 0, h - 1)
        y_end = _clamp(y_end, 1, h)

        # Ensure valid slice
        if x_end <= x_start or y_end <= y_start:
            raise ValueError(f"Invalid ROI bounds for {name}: {(x_start, y_start, x_end, y_end)}")

        rois[name] = card_image[y_start:y_end, x_start:x_end]

    return rois
