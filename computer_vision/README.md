# Computer Vision Module

## Overview

Image preprocessing and barcode detection module for the Automated Self-Service Student ID Card Issuance System. Handles image capture, preprocessing pipeline (grayscale conversion, resizing, ROI extraction), and barcode scanning for card identification and verification.

---

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

Ensure `opencv-python`, `pyzbar`, and `pillow` are installed in your environment.

---

## Module Structure

```bash
computer_vision/
├── core/              # Core CV functions (image_utils, barcode_reader)
├── pipeline/          # Processing pipeline orchestration
├── config/            # Configuration files (camera, processing params)
├── tests/             # Manual and automated tests
├── data/              # Sample images, debug outputs, calibration data
├── docs/              # API reference, setup guides
└── utils/             # Logging, file I/O helpers
```

---

## Implementation Status

**Overall Progress: 14%** (6 phases)

**Phase 1: Environment Setup** 🚧 68%

- ✅ Software installation complete
- ✅ Development environment configured
- ⏳ Camera hardware acquisition pending
- ✅ Test data partially prepared

**Phase 2: Image Capture** ⏳ 0%

- ⏳ Camera configuration
- ⏳ Camera interface implementation
- ⏳ Testing suite

**Phase 3: Image Preprocessing** 🚧 16%

- ✅ Basic preprocessing functions (grayscale, resize, ROI crop)
- ⏳ Advanced preprocessing (blur, thresholding, morphology)
- ⏳ Processing pipeline
- ⏳ Testing suite

**Phase 4: Barcode Detection** ⏳ 0%

- ⏳ Barcode detection
- ⏳ Barcode decoding
- ⏳ Edge case handling
- ⏳ Testing suite

**Phase 5: Error Handling** ⏳ 0%

- ⏳ Custom exceptions
- ⏳ Exception integration
- ⏳ Retry logic

**Phase 6: Integration & Testing** ⏳ 0%

- ⏳ Public API
- ⏳ Database integration
- ⏳ End-to-end testing
- ⏳ Performance benchmarking

---

## Data Organization

### Input Images

Place sample ID card images in:

```bash
data/sample_barcodes/
```

### Debug Outputs

Processed images saved to:

```bash
data/debug_outputs/
```

Includes intermediate preprocessing results for visual inspection.

---

## Dependencies

See [requirements.txt](requirements.txt) for full list.

---

## Notes & Limitations

- **No camera integration yet**: Works with static images only
- **Fixed orientation**: Assumes cards are consistently oriented
- **ROI hardcoded**: Bottom-half crop; configurable in future iterations
- **Testing environment**: Local development with mock data; not production-ready
