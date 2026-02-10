# OCR Setup Guide

## Overview

This guide explains how to install dependencies and set up the OCR module for the ID card system.

## 1. System Requirements

- Linux with Python 3.10+
- OpenCV and Tesseract OCR installed
- Camera or image files for testing

## 2. Install Tesseract

Install Tesseract and the English language pack using your package manager.

## 3. Python Environment

Create/activate your Python environment and install requirements:

- `pytesseract`
- `opencv-python`
- `numpy`

## 4. Configuration

Update [computer_vision/config/ocr_config.py](computer_vision/config/ocr_config.py) if needed:

- Anchor text and ROI offsets
- Student ID regex pattern
- Tesseract config and preprocessing parameters

## 5. Test Images

Add test images to [computer_vision/data/test_cards](computer_vision/data/test_cards).

## 6. Run Manual Tests

- Student ID OCR: [computer_vision/tests/manual_tests/test_student_id_ocr.py](computer_vision/tests/manual_tests/test_student_id_ocr.py)
- Preprocessing preview: [computer_vision/tests/manual_tests/test_preprocessing.py](computer_vision/tests/manual_tests/test_preprocessing.py)

## 7. Troubleshooting

- If no card is detected, adjust lighting and card position.
- If OCR fails, tune preprocessing and PSM settings in config.
