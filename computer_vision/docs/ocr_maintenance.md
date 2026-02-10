# OCR Maintenance Guide

## 1. Updating ROI Coordinates

If card design changes, update anchor offsets in [computer_vision/config/ocr_config.py](computer_vision/config/ocr_config.py) and re-test:

- Use [computer_vision/tests/manual_tests/test_anchor_roi_extraction.py](computer_vision/tests/manual_tests/test_anchor_roi_extraction.py) or visual tools.

## 2. Tesseract Tuning

- Keep PSM at the best-performing value (currently 6).
- Adjust `char_whitelist` if format changes.

## 3. Preprocessing Tweaks

- Toggle binarization/contrast/denoise in config.
- Re-run [computer_vision/tests/manual_tests/test_preprocessing.py](computer_vision/tests/manual_tests/test_preprocessing.py) after changes.

## 4. Monitoring Performance

- Run [computer_vision/tests/manual_tests/benchmark_pipeline.py](computer_vision/tests/manual_tests/benchmark_pipeline.py) periodically.
- Investigate failures in [computer_vision/tests/test_ocr_pipeline.py](computer_vision/tests/test_ocr_pipeline.py).

## 5. Logs and Debug Images

- Enable `DEBUG.verbose_logging` for console logs.
- Save intermediate outputs using the manual tests for visual checks.
