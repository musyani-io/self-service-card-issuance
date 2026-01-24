# Computer Vision Implementation Guideline

## Project: ID Card Kiosk - Computer Vision Module

**Purpose:** Complete task list for implementing the barcode scanning system for automated ID card dispensing.

**Estimated Total Time:** 3-4 weeks (working part-time)

---

## Phase 1: Environment Setup & Hardware Preparation

**Goal:** Get all tools and hardware ready for CV development

### Task 1.1: Install Required Software

- [ ] Update Raspberry Pi OS to latest version
- [x] Install Python 3.9 or higher
- [x] Install OpenCV library (`python3-opencv`)
- [x] Install pyzbar library for barcode reading
- [x] Install Pillow for image handling
- [x] Install picamera2 (if using Pi Camera Module)
- [ ] Verify all installations with version checks

**Success Criteria:** All libraries import without errors in Python

**Estimated Time:** 1 hour

---

### Task 1.2: Acquire and Connect Camera Hardware

- [ ] Purchase/obtain Raspberry Pi Camera Module 3 (or USB webcam)
- [ ] Physically mount camera to Raspberry Pi
- [ ] Enable camera interface in Raspberry Pi configuration
- [ ] Test camera connection with basic capture command
- [ ] Verify image quality and focus

**Success Criteria:** Camera captures clear images, saves to file successfully

**Estimated Time:** 2 hours

---

### Task 1.3: Set Up Development Environment

- [x] Create project directory structure (as defined)
- [x] Initialize Git repository (optional but recommended)
- [x] Create virtual environment for Python dependencies
- [x] Create `requirements.txt` file with all dependencies
- [x] Set up IDE/editor (VS Code, Thonny, or preferred)

**Success Criteria:** Directory structure matches specification, can run Python scripts from project root

**Estimated Time:** 30 minutes

---

### Task 1.4: Prepare Test Data

- [ ] Obtain 5-10 sample ID cards (with permission) OR create mock cards with barcodes
- [ ] Photograph sample cards at various angles (0°, 15°, 30°)
- [ ] Photograph cards under different lighting conditions
- [ ] Save images to `data/sample_barcodes/` directory
- [ ] Document each image (filename format: `card_ID_angle_lighting.jpg`)

**Success Criteria:** At least 20 test images captured and organized

**Estimated Time:** 2 hours

---

## Phase 2: Core Functionality - Image Capture

**Goal:** Implement reliable camera interface

### Task 2.1: Create Camera Configuration

- [ ] Define camera parameters in `config/camera_config.py`
- [ ] Set resolution (start with 1280x720)
- [ ] Set frame rate (15-30 fps)
- [ ] Define exposure and brightness defaults
- [ ] Add camera type selection (Pi Camera vs USB)

**Success Criteria:** Configuration file loads without errors, parameters are accessible

**Estimated Time:** 30 minutes

---

### Task 2.2: Implement Basic Camera Interface

- [ ] Create `image_capture.py` file
- [ ] Write function to initialize camera based on type
- [ ] Write function to capture single frame
- [ ] Write function to save captured frame to file
- [ ] Write function to release camera resources
- [ ] Add error handling for camera connection failures

**Success Criteria:** Can capture and save image programmatically

**Estimated Time:** 2 hours

---

### Task 2.3: Test Camera Module

- [ ] Create `tests/test_image_capture.py`
- [ ] Write test for camera initialization
- [ ] Write test for frame capture
- [ ] Write test for camera release
- [ ] Run all tests and verify they pass
- [ ] Fix any bugs discovered

**Success Criteria:** All camera tests pass, no resource leaks

**Estimated Time:** 1 hour

---

## Phase 3: Image Preprocessing

**Goal:** Prepare images for reliable barcode detection

### Task 3.1: Implement Basic Preprocessing Functions

- [x] Create `image_utils.py` file
- [x] Write function to convert image to grayscale
- [x] Write function to resize image (maintain aspect ratio)
- [x] Write function to crop image to region of interest
- [x] Write function to save debug images with annotations

**Success Criteria:** Each function works independently with test images

**Estimated Time:** 2 hours

---

### Task 3.2: Implement Advanced Preprocessing

- [x] Add Gaussian blur function (reduce noise)
- [x] Add adaptive thresholding function (handle lighting variations)
- [x] Add morphological operations (close gaps in barcode lines)
- [x] Add contrast enhancement function
- [x] Test each function on sample images, compare before/after

**Success Criteria:** Preprocessing improves barcode visibility in poor-quality images

**Estimated Time:** 3 hours

---

### Task 3.3: Create Preprocessing Pipeline

- [x] Write function that chains preprocessing steps
- [x] Make pipeline configurable (enable/disable specific steps)
- [x] Add timing measurements to identify slow operations
- [x] Optimize processing order for best results
- [x] Document which preprocessing helps which image problems

**Success Criteria:** Pipeline processes image in under 200ms

**Estimated Time:** 2 hours

---

### Task 3.4: Test Image Utilities

- [x] Create `tests/test_image_utils.py`
- [x] Test each preprocessing function individually
- [x] Test full pipeline with various image qualities
- [x] Verify output images are valid
- [x] Run all tests and fix bugs

**Success Criteria:** All preprocessing tests pass

**Estimated Time:** 1.5 hours

---

## Phase 4: Barcode Detection & Decoding

**Goal:** Reliably find and read barcodes from ID cards

### Task 4.1: Implement Basic Barcode Detection

- [ ] Create `barcode_reader.py` file
- [ ] Write function to detect barcode location in image (using pyzbar)
- [ ] Extract bounding box coordinates (x, y, width, height)
- [ ] Return confidence score if available
- [ ] Handle case where no barcode is found

**Success Criteria:** Detects barcode location in 90%+ of test images

**Estimated Time:** 2 hours

---

### Task 4.2: Implement Barcode Decoding

- [ ] Write function to decode barcode data from image
- [ ] Extract barcode string (student ID)
- [ ] Extract barcode type (Code128, QR, etc.)
- [ ] Validate decoded data format
- [ ] Handle decoding failures gracefully

**Success Criteria:** Decodes barcode data correctly from clear images

**Estimated Time:** 1.5 hours

---

### Task 4.3: Combine Detection + Decoding

- [ ] Write combined function: `scan_card(image)`
- [ ] Integrate preprocessing pipeline before detection
- [ ] Return structured result: `{barcode_id, type, bbox, confidence}`
- [ ] Add retry logic with different preprocessing (if first attempt fails)
- [ ] Log all scan attempts and results

**Success Criteria:** Single function call reliably returns barcode data

**Estimated Time:** 2 hours

---

### Task 4.4: Handle Edge Cases

- [ ] Handle multiple barcodes in single image
- [ ] Handle partially visible barcodes
- [ ] Handle damaged/worn barcodes
- [ ] Add minimum confidence threshold
- [ ] Implement maximum retry attempts (3 retries)

**Success Criteria:** System handles edge cases without crashing

**Estimated Time:** 2 hours

---

### Task 4.5: Test Barcode Reader

- [ ] Create `tests/test_barcode_reader.py`
- [ ] Test detection with clear images
- [ ] Test detection with poor lighting
- [ ] Test detection with angled cards
- [ ] Test decoding accuracy
- [ ] Test edge case handling
- [ ] Run all tests and fix bugs

**Success Criteria:** 95%+ detection rate on test dataset

**Estimated Time:** 2 hours

---

## Phase 5: Error Handling & Robustness

**Goal:** Make system resilient to failures

### Task 5.1: Define Custom Exceptions

- [ ] Create `exceptions.py` file
- [ ] Define `BarcodeNotFoundError` exception
- [ ] Define `MultipleBarcodeError` exception
- [ ] Define `BarcodeDecodeError` exception
- [ ] Define `CameraError` exception
- [ ] Add descriptive error messages for each

**Success Criteria:** All custom exceptions defined and importable

**Estimated Time:** 30 minutes

---

### Task 5.2: Integrate Exception Handling

- [ ] Update `barcode_reader.py` to raise appropriate exceptions
- [ ] Update `image_capture.py` to raise `CameraError` on failures
- [ ] Add try-except blocks around all CV operations
- [ ] Log exceptions with full context (timestamp, image path, error details)
- [ ] Test that exceptions propagate correctly to caller

**Success Criteria:** System provides clear error messages for all failure modes

**Estimated Time:** 2 hours

---

### Task 5.3: Implement Retry Logic

- [ ] Create retry wrapper function (max 3 attempts)
- [ ] Add progressive backoff (wait 0.5s between retries)
- [ ] Try different preprocessing on each retry
- [ ] Log each retry attempt
- [ ] Return detailed failure report after exhausting retries

**Success Criteria:** System automatically recovers from temporary failures

**Estimated Time:** 1.5 hours

---

## Phase 6: System Integration & Testing

**Goal:** Integrate CV module with main system

### Task 6.1: Create Public API

- [ ] Update `computer_vision/__init__.py`
- [ ] Export main functions: `scan_card()`, `verify_card()`
- [ ] Create simple usage examples
- [ ] Document expected input/output formats
- [ ] Version the API (v1.0)

**Success Criteria:** High-level controller can import and use CV functions easily

**Estimated Time:** 1 hour

---

### Task 6.2: Integration with Database

- [ ] Define data structure for card mapping: `{slot_index: barcode_id}`
- [ ] Write function to scan card and return mapping data
- [ ] Write function to verify card matches expected barcode
- [ ] Add database logging for all scan operations
- [ ] Test database writes and reads

**Success Criteria:** CV scan results successfully stored in database

**Estimated Time:** 2 hours

---

### Task 6.3: Create End-to-End Test

- [ ] Simulate staff card loading workflow
- [ ] Scan 10 cards, store mappings
- [ ] Simulate student retrieval workflow
- [ ] Verify each card against expected barcode
- [ ] Measure total time for complete workflow
- [ ] Document any failures or issues

**Success Criteria:** Complete workflow executes without manual intervention

**Estimated Time:** 2 hours

---

### Task 6.4: Performance Benchmarking

- [ ] Measure average scan time (target: <500ms)
- [ ] Measure detection success rate (target: >95%)
- [ ] Measure false positive rate (target: <2%)
- [ ] Test under different lighting conditions
- [ ] Test with 50+ different barcode images
- [ ] Document results in `docs/performance_benchmarks.md`

**Success Criteria:** System meets or exceeds performance targets

**Estimated Time:** 3 hours

---

## Phase 7: Camera Calibration & Optimization

**Goal:** Maximize accuracy and speed

### Task 7.1: Camera Calibration

- [ ] Print checkerboard calibration pattern (9x6 or similar)
- [ ] Capture 20+ images of checkerboard at different angles
- [ ] Save images to `data/calibration_images/`
- [ ] Run OpenCV calibration algorithm
- [ ] Extract intrinsic matrix and distortion coefficients
- [ ] Save calibration data to `config/calibration_data.json`

**Success Criteria:** Camera calibration completes, distortion correction works

**Estimated Time:** 3 hours

---

### Task 7.2: Apply Calibration to Pipeline

- [ ] Load calibration data on system startup
- [ ] Apply lens distortion correction to captured images
- [ ] Compare barcode detection before/after correction
- [ ] Measure performance improvement
- [ ] Make calibration optional (config flag)

**Success Criteria:** Calibrated system detects barcodes more reliably at angles

**Estimated Time:** 2 hours

---

### Task 7.3: Optimize Processing Speed

- [ ] Profile code to find bottlenecks (use cProfile)
- [ ] Reduce image resolution if possible (test 640x480)
- [ ] Process only region of interest (crop before processing)
- [ ] Cache preprocessed images if multiple operations needed
- [ ] Optimize preprocessing pipeline order
- [ ] Measure speed improvement

**Success Criteria:** Processing time reduced by 30%+ without accuracy loss

**Estimated Time:** 3 hours

---

## Phase 8: Documentation & Deployment Prep

**Goal:** Prepare system for deployment and handover

### Task 8.1: Write Setup Guide

- [ ] Create `docs/cv_setup_guide.md`
- [ ] Document camera installation procedure
- [ ] Document lighting setup requirements
- [ ] Document calibration procedure
- [ ] Include troubleshooting section
- [ ] Add photos/diagrams of proper setup

**Success Criteria:** Someone unfamiliar with the project can set up CV system using guide

**Estimated Time:** 3 hours

---

### Task 8.2: Create API Reference

- [ ] Document all public functions in `__init__.py`
- [ ] Include function signatures, parameters, return values
- [ ] Add usage examples for each function
- [ ] Document all custom exceptions
- [ ] Explain configuration options
- [ ] Save as `docs/cv_api_reference.md`

**Success Criteria:** Complete API documentation available

**Estimated Time:** 2 hours

---

### Task 8.3: Final System Validation

- [ ] Run all unit tests, ensure 100% pass
- [ ] Run integration tests with real hardware
- [ ] Test with 100+ barcode scans
- [ ] Verify error handling works correctly
- [ ] Test recovery from camera disconnection
- [ ] Document any known limitations

**Success Criteria:** System validated and ready for deployment

**Estimated Time:** 3 hours

---

### Task 8.4: Code Cleanup & Review

- [ ] Remove debug print statements
- [ ] Remove unused imports
- [ ] Add docstrings to all functions
- [ ] Format code with Black or autopep8
- [ ] Run linter (pylint) and fix issues
- [ ] Update `requirements.txt` with exact versions

**Success Criteria:** Code is clean, documented, and follows Python best practices

**Estimated Time:** 2 hours

---

## Phase 9: Optional Enhancements

**Goal:** Additional features if time permits

### Task 9.1: Add Logging Dashboard (Optional)

- [ ] Create simple visualization of scan success/failure rates
- [ ] Display average processing time
- [ ] Show most common failure modes
- [ ] Generate daily/weekly reports

**Estimated Time:** 4 hours

---

### Task 9.2: Implement Card Quality Check (Optional)

- [ ] Detect if card is damaged or defaced
- [ ] Check if barcode area is obscured
- [ ] Warn staff about low-quality cards during mapping
- [ ] Log quality metrics

**Estimated Time:** 3 hours

---

### Task 9.3: Add Multi-Threading (Optional)

- [ ] Separate camera capture and image processing into different threads
- [ ] Implement frame buffer for continuous capture
- [ ] Reduce latency between trigger and result
- [ ] Test thread safety

**Estimated Time:** 4 hours

---

## Completion Checklist

**Minimum Viable Product (MVP):**

- [ ] All Phase 1-6 tasks completed
- [ ] System scans barcodes reliably (>90% success rate)
- [ ] Error handling works correctly
- [ ] Integration with database functional
- [ ] Basic documentation complete

**Full Production System:**

- [ ] All Phase 1-8 tasks completed
- [ ] Camera calibrated and optimized
- [ ] Comprehensive documentation available
- [ ] System validated with real hardware
- [ ] Performance meets all targets

**Enhanced System (If Time Allows):**

- [ ] Phase 9 optional tasks completed
- [ ] Additional features implemented
- [ ] Advanced error recovery mechanisms

---

## Progress Tracking

**Week 1:** Phases 1-2 (Setup + Basic Capture)  
**Week 2:** Phases 3-4 (Preprocessing + Barcode Reading)  
**Week 3:** Phases 5-6 (Error Handling + Integration)  
**Week 4:** Phases 7-8 (Calibration + Documentation)

---

## Notes

- Each task should be marked complete only when success criteria are met
- If stuck on a task for >4 hours, document the blocker and seek help
- Test frequently - don't wait until end to discover issues
- Prioritize reliability over speed initially
- Document decisions and trade-offs as you go

---

**Good luck with implementation!**
