# Computer Vision Module

This module provides computer vision functionality for the Self-Service Card Issuance system, specifically focused on capturing, validating, and processing student ID card images for barcode detection and decoding.

## Overview

The computer vision module handles the complete image processing pipeline:

- Camera initialization and frame capture
- Image quality validation
- Barcode detection and decoding
- Automatic retry and error handling
- Performance metrics and monitoring

## Module Structure

```bash
computer_vision/
├── __init__.py              # Module initialization
├── barcode_reader.py        # Barcode detection and decoding
├── image_capture.py         # Camera hardware interface
├── image_utils.py           # Image processing utilities
├── quality_validator.py     # Image quality validation
├── retry_handler.py         # Retry logic for failed operations
├── exceptions.py            # Custom exception classes
├── logging_config.py        # Logging configuration
├── metrics.py               # Performance metrics tracking
├── cv_guideline.md          # Development guidelines
├── calibration/             # Camera calibration utilities
│   ├── __init__.py
│   └── exposure_optimizer.py
├── config/                  # Configuration modules
│   ├── __init__.py
│   └── camera_config.py
├── data/                    # Sample and calibration data
│   ├── calibration_images/
│   └── sample_barcodes/
└── tests/                   # Unit tests
    ├── __init__.py
    ├── test_barcode_reader.py
    ├── test_image_capture.py
    ├── test_image_utils.py
    ├── test_quality_validator.py
    └── test_retry_handler.py
```

## Dependencies

This module requires the following Python packages:

- `opencv-python` - Image processing and computer vision
- `numpy` - Numerical operations on image arrays
- `pyzbar` - Barcode detection and decoding
- `picamera2` - Raspberry Pi camera interface
- `pillow` - Image manipulation utilities

See `../requirements.txt` for complete dependency list.

## Calibration

The `calibration/` directory contains tools for optimizing camera settings:

- `exposure_optimizer.py` - Automatic exposure adjustment for optimal barcode reading

Calibration images can be stored in `data/calibration_images/` for reference and testing.

## Error Handling

The module implements robust error handling through:

- Custom exceptions defined in `exceptions.py`
- Automatic retry logic in `retry_handler.py`
- Comprehensive logging via `logging_config.py`

## Performance Monitoring

Performance metrics are tracked using the `metrics.py` module, including:

- Frame capture time
- Barcode decode time
- Quality validation time
- Success/failure rates

## Development Guidelines

For detailed development guidelines and coding standards, see [cv_guideline.md](cv_guideline.md).

## Integration

This module is designed to integrate with the Raspberry Pi hardware system in the `raspberry-pi/` directory. The main workflow orchestrates computer vision operations for the self-service kiosk.
