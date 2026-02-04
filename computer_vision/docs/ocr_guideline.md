# OCR Implementation Guideline for ID Card System

## Project: Self-Service Student ID Card Issuance - OCR Module

**Purpose:** Step-by-step guide for implementing an OCR-based student ID extraction system to replace the failed barcode detection approach.

**Estimated Total Time:** 2-3 weeks (working part-time)

---

## Overview of OCR Approach

Instead of relying on barcode scanning, we will use **Optical Character Recognition (OCR)** to directly read the student ID number printed on the card. This approach is more robust and doesn't depend on barcode quality.

### Pipeline Architecture

```
Raw Image → Card Detection → Perspective Correction → ROI Extraction → OCR → Student ID
```

**Key Advantages:**

- No dependency on barcode quality or printing
- More robust to card orientation and lighting
- Can extract additional information (name, program, etc.)
- Provides fallback if one text region is damaged

---

## Phase 1: Environment Setup & Testing

### Task 1.1: Install OCR Dependencies

**Goal:** Set up Tesseract OCR engine and Python bindings

**Steps:**

- [x] Update system packages

  ```bash
  sudo apt-get update
  sudo apt-get upgrade
  ```

- [x] Install Tesseract OCR engine

  ```bash
  sudo apt-get install tesseract-ocr
  sudo apt-get install tesseract-ocr-eng  # English language pack
  ```

- [x] Verify Tesseract installation

  ```bash
  tesseract --version
  # Should show version 4.x or 5.x
  ```

- [x] Install Python OCR library

  ```bash
  cd /path/to/project
  source .venv/bin/activate
  pip install pytesseract==0.3.13
  ```

- [x] Test pytesseract import

  ```python
  python3 -c "import pytesseract; print('Success!')"
  ```

**Success Criteria:** Tesseract and pytesseract are installed and importable

**Estimated Time:** 30 minutes

---

### Task 1.2: Prepare Test Card Images

**Goal:** Create a diverse dataset for testing OCR accuracy

**Steps:**

- [x] Collect 10-15 sample ID cards (with permission)
- [x] Photograph cards at different conditions:
  - Various distances: 20cm, 30cm, 40cm
  - Various angles: 0°, 15°, 30°, 45°
  - Different lighting: bright, dim, natural light, artificial light
  - Different orientations: portrait, landscape, slightly rotated
- [x] Save images to `data/test_cards/`
- [x] Document card layout:
  - Where is the student ID located? (top, middle, bottom)
  - What format? (e.g., "2020-04-12345" or "2020/04/12345")
  - What font is used?
  - Are there any special characters or patterns?

**Success Criteria:** At least 30 test images with varied conditions

**Estimated Time:** 2 hours

---

### Task 1.3: Understand Your Card Layout

**Goal:** Document the exact structure of your university's ID cards

**Steps:**

- [x] Create a reference document (`docs/card_layout.md`) with:
  - Physical dimensions of the card
  - Location of student ID text (measure from top-left corner)
  - Student ID format (exact regex pattern)
  - Location of other useful text (name, program, year)
  - Font characteristics
  - Background color/pattern in text regions
- [x] Take a high-quality scan of one card
- [x] Mark ROI coordinates on the image using an image editor
- [x] Document typical variations (older cards vs newer cards)

**Success Criteria:** Clear documentation of card layout with measurements

**Estimated Time:** 1 hour

---

## Phase 2: Card Detection

### Task 2.1: Implement Basic Card Detection

**Goal:** Detect the physical card in the image and extract its boundary

**File to create:** `computer_vision/core/card_detector.py`

**Steps:**

- [x] Create the file with basic structure
- [x] Implement preprocessing:
  - Convert to grayscale
  - Apply Gaussian blur (kernel size 5x5)
  - Apply Canny edge detection (thresholds: 50, 150)
- [x] Implement contour detection:
  - Find all contours using `cv2.findContours()`
  - Sort contours by area (largest first)
  - Filter contours by:
    - Minimum area (e.g., 10,000 pixels)
    - Number of sides (should be 4 for rectangular card)
    - Aspect ratio (ID cards are typically 1.586:1, CR80 standard)
- [x] Implement corner detection:
  - Use `cv2.approxPolyDP()` to get 4 corner points
  - Return corners in order: top-left, top-right, bottom-right, bottom-left
- [x] Add error handling for:
  - No card found
  - Multiple cards detected
  - Invalid card shape

**Function signature:**

```python
def detect_card(image: np.ndarray) -> Optional[np.ndarray]:
    \"\"\"
    Detect ID card in image

    Args:
        image: Input image (BGR format)

    Returns:
        Array of 4 corner points [(x,y), (x,y), (x,y), (x,y)]
        or None if no card detected
    \"\"\"
```

**Success Criteria:**

- Detects card in 90%+ of test images
- Returns correct 4 corner points
- Handles edge cases gracefully

**Estimated Time:** 3 hours

---

### Task 2.2: Test Card Detection

**Goal:** Validate card detection works reliably

**File to create:** `computer_vision/tests/manual_tests/test_card_detection.py`

**Steps:**

- [x] Create test script that:
  - Loads test images from `data/test_cards/`
  - Runs card detection on each
  - Draws detected corners on the image
  - Saves annotated images to `data/detection_results/`
  - Prints success/failure statistics
- [x] Run tests on all images
- [x] Analyze failures:
  - Document which lighting conditions fail
  - Document which angles fail
  - Note any patterns
- [x] Adjust detection parameters based on results:
  - Canny thresholds
  - Minimum area
  - Aspect ratio tolerance
- [x] Re-test until 90%+ success rate

**Success Criteria:** 90%+ detection rate on test dataset

**Estimated Time:** 2 hours

---

## Phase 3: Perspective Correction

### Task 3.1: Implement Perspective Transform

**Goal:** Convert detected card to a top-down, straightened view

**File to create:** `computer_vision/core/perspective_corrector.py`

**Steps:**

- [x] Create helper function to order corner points consistently

  ```python
  def order_points(corners):
      # Order: top-left, top-right, bottom-right, bottom-left
  ```

- [x] Implement perspective transformation:
  - Calculate output dimensions based on corner distances
  - Create destination rectangle coordinates
  - Compute perspective transformation matrix using `cv2.getPerspectiveTransform()`
  - Apply transformation using `cv2.warpPerspective()`
- [x] Handle aspect ratio preservation:
  - Ensure output matches standard ID card ratio (85.60mm × 53.98mm = 1.586:1)
  - Resize to standard resolution (e.g., 856 × 539 pixels)
- [x] Add quality checks:
  - Verify output is not too distorted
  - Check for black borders (indicate bad transformation)

**Function signature:**

```python
def straighten_card(image: np.ndarray, corners: np.ndarray) -> np.ndarray:
    \"\"\"
    Apply perspective transform to get top-down view of card

    Args:
        image: Original image
        corners: 4 corner points of card

    Returns:
        Straightened card image (standardized size)
    \"\"\"
```

**Success Criteria:**

- Produces straight, rectangular card images
- Maintains text readability
- Consistent output size

**Estimated Time:** 2 hours

---

### Task 3.2: Test Perspective Correction

**Goal:** Verify perspective correction works correctly

**File to create:** `computer_vision/tests/manual_tests/test_perspective.py`

**Steps:**

- [x] Create test script that:
  - Detects card
  - Applies perspective correction
  - Saves straightened card images
- [x] Visual inspection of results:
  - Text should be horizontal and readable
  - No excessive distortion
  - Aspect ratio looks correct
- [x] Measure output dimensions
- [x] Test with extreme angles (30°, 45°)

**Success Criteria:** Straightened cards are readable and properly oriented

**Estimated Time:** 1 hour

---

## Phase 4: ROI Extraction

### Task 4.1: Define ROI Regions

**Goal:** Extract specific regions containing student ID and other text

**File to create:** `computer_vision/core/roi_extractor.py`

**Steps:**

- [ ] Based on your card layout documentation, define ROI coordinates
  - Student ID region (primary)
  - Name region (optional, for validation)
  - Program/year region (optional)
- [ ] Implement ROI extraction function using array slicing
- [ ] Add configuration file for ROI parameters:
  - Create `config/ocr_config.py`
  - Define ROI as ratios of card dimensions:

    ```python
    STUDENT_ID_ROI = {
        'x_start': 0.10,  # 10% from left
        'x_end': 0.90,    # 90% from left
        'y_start': 0.30,  # 30% from top
        'y_end': 0.45     # 45% from top
    }
    ```

- [ ] Make ROI extraction configurable for different card layouts

**Function signature:**

```python
def extract_roi(card_image: np.ndarray,
                roi_config: Dict) -> Dict[str, np.ndarray]:
    \"\"\"
    Extract region of interest from straightened card

    Args:
        card_image: Straightened card image
        roi_config: Dictionary with ROI coordinates

    Returns:
        Dictionary mapping region name to cropped image
        e.g., {'student_id': np.ndarray, 'name': np.ndarray}
    \"\"\"
```

**Success Criteria:**

- Extracted ROIs contain the target text
- Minimal background/noise in ROIs
- Works across different card orientations

**Estimated Time:** 2 hours

---

### Task 4.2: Test ROI Extraction

**Goal:** Verify ROI coordinates are correct

**File to create:** `computer_vision/tests/manual_tests/test_roi_extraction.py`

**Steps:**

- [ ] Create test script that:
  - Processes cards through detection → straightening → ROI extraction
  - Saves each ROI as separate image
  - Annotates original card with ROI boundaries
- [ ] Visual verification:
  - Check that student ID is fully visible in extracted ROI
  - Verify no important text is cut off
  - Ensure minimal background noise
- [ ] Test with 10+ different cards
- [ ] Adjust ROI coordinates if needed
- [ ] Document final ROI parameters

**Success Criteria:** Student ID is centered and complete in extracted ROI

**Estimated Time:** 1.5 hours

---

## Phase 5: Image Preprocessing for OCR

### Task 5.1: Implement OCR-Specific Preprocessing

**Goal:** Enhance ROI images to maximize OCR accuracy

**File to update:** `computer_vision/core/image_utils.py`

**Steps:**

- [ ] Add preprocessing functions:

  **Contrast Enhancement:**

  ```python
  def enhance_contrast(image: np.ndarray) -> np.ndarray:
      # Use CLAHE (Contrast Limited Adaptive Histogram Equalization)
  ```

  **Denoising:**

  ```python
  def denoise_image(image: np.ndarray) -> np.ndarray:
      # Use fastNlMeansDenoising
  ```

  **Binarization:**

  ```python
  def binarize_image(image: np.ndarray) -> np.ndarray:
      # Use adaptive thresholding or Otsu's method
  ```

  **Deskewing (if text is slightly tilted):**

  ```python
  def deskew_text(image: np.ndarray) -> np.ndarray:
      # Detect text angle and rotate
  ```

- [ ] Create preprocessing pipeline:

  ```python
  def preprocess_for_ocr(roi: np.ndarray) -> np.ndarray:
      # Chain: grayscale → denoise → enhance → binarize → deskew
  ```

- [ ] Make pipeline configurable (enable/disable specific steps)

**Success Criteria:**

- Preprocessed images have clear, high-contrast text
- Background noise is minimized
- Text edges are sharp

**Estimated Time:** 3 hours

---

### Task 5.2: Test Preprocessing Quality

**Goal:** Compare OCR results with and without preprocessing

**File to create:** `computer_vision/tests/manual_tests/test_preprocessing.py`

**Steps:**

- [ ] Create test script that shows before/after:
  - Original ROI
  - After each preprocessing step
  - Final preprocessed image
- [ ] Save comparison images
- [ ] Visual inspection of text clarity
- [ ] Try different preprocessing combinations
- [ ] Benchmark which combination works best:
  - Test on 5 sample cards
  - Try different orders of operations
  - Document best pipeline

**Success Criteria:** Clear improvement in text visibility

**Estimated Time:** 2 hours

---

## Phase 6: OCR Implementation

### Task 6.1: Implement Basic OCR

**Goal:** Extract text from preprocessed ROI

**File to create:** `computer_vision/core/ocr_reader.py`

**Steps:**

- [ ] Import pytesseract
- [ ] Implement basic OCR function:

  ```python
  def extract_text(roi: np.ndarray,
                   config: str = '') -> str:
      \"\"\"Extract raw text from ROI using Tesseract\"\"\"
  ```

- [ ] Configure Tesseract for ID cards:
  - Page segmentation mode (PSM): Try PSM 6 (uniform block) or PSM 7 (single line)
  - OCR Engine Mode (OEM): Use OEM 3 (default)
  - Whitelist characters (only allow digits, letters, hyphens):

    ```python
    config = '--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-/'
    ```

- [ ] Test different Tesseract configurations:
  - PSM 3, 6, 7, 11
  - Different whitelists
  - Different OEM modes
  - Document which works best

**Success Criteria:**

- Can extract text from clear ROI images
- Minimal garbage characters in output

**Estimated Time:** 2 hours

---

### Task 6.2: Implement Student ID Extraction

**Goal:** Parse raw OCR text to extract valid student ID

**Steps:**

- [ ] Define student ID pattern (regex):
  - Based on your card format documentation
  - Example: `r'\\d{4}-\\d{2}-\\d{5}'` for format "2020-04-12345"
  - Or: `r'\\d{4}/\\d{2}/\\d{5}'` for format "2020/04/12345"
  - Make it configurable in `config/ocr_config.py`

- [ ] Implement extraction function:

  ```python
  def extract_student_id(roi: np.ndarray) -> Optional[str]:
      \"\"\"
      Extract and validate student ID from ROI

      Returns:
          Student ID string or None if not found
      \"\"\"
      # 1. Preprocess ROI
      # 2. Run OCR
      # 3. Apply regex to extract ID
      # 4. Validate format
      # 5. Return first valid match
  ```

- [ ] Add validation checks:
  - Length validation
  - Year range validation (e.g., 2015-2030)
  - Checksum validation (if your IDs have checksums)

- [ ] Handle common OCR errors:
  - "O" vs "0" (letter O vs zero)
  - "I" vs "1" (letter I vs one)
  - "S" vs "5"
  - Implement character correction logic

**Success Criteria:**

- Correctly extracts student ID from clear images
- Filters out invalid patterns
- Robust to common OCR mistakes

**Estimated Time:** 3 hours

---

### Task 6.3: Implement Retry Logic

**Goal:** Improve accuracy through multiple extraction attempts

**Steps:**

- [ ] Implement retry mechanism with different strategies:

  **Strategy 1:** Original preprocessing
  **Strategy 2:** Higher contrast
  **Strategy 3:** Different binarization threshold
  **Strategy 4:** Different Tesseract PSM mode
  **Strategy 5:** Inverted image (white text on black background)

- [ ] Implement voting system:
  - Run 3-5 extraction attempts with different strategies
  - If multiple attempts return the same ID, use that (high confidence)
  - If all differ, return most common or flag for manual review

- [ ] Add confidence scoring:
  - Based on Tesseract confidence scores
  - Based on regex match strength
  - Based on voting consensus

```python
def extract_student_id_robust(roi: np.ndarray,
                                max_retries: int = 3) -> Dict:
    \"\"\"
    Extract student ID with retry logic

    Returns:
        {
            'student_id': str or None,
            'confidence': float,
            'method': str
        }
    \"\"\"
```

**Success Criteria:**

- Increased accuracy through retries
- Clear confidence metrics

**Estimated Time:** 3 hours

---

## Phase 7: Integration & Testing

### Task 7.1: Create Complete OCR Pipeline

**Goal:** Integrate all components into single pipeline

**File to create:** `computer_vision/pipeline/ocr_pipeline.py`

**Steps:**

- [ ] Create pipeline class:

  ```python
  class CardOCRPipeline:
      def __init__(self, config: Dict):
          # Initialize components

      def scan_card(self, image: np.ndarray) -> Dict:
          \"\"\"
          Complete pipeline: detection → correction → ROI → OCR

          Returns:
              {
                  'success': bool,
                  'student_id': str or None,
                  'confidence': float,
                  'method': str,
                  'error': str or None,
                  'processing_time_ms': float
              }
          \"\"\"
  ```

- [ ] Implement full pipeline flow:
  1. Detect card (raise CardNotFoundError if failed)
  2. Apply perspective correction
  3. Extract ROI
  4. Preprocess ROI
  5. Extract student ID with retries
  6. Return structured result

- [ ] Add comprehensive logging:
  - Log each pipeline stage
  - Log processing times
  - Log confidence scores
  - Save debug images (optional)

- [ ] Add timing measurements:
  - Measure total processing time
  - Measure per-stage time
  - Optimize if > 1 second

**Success Criteria:**

- Single function call processes complete workflow
- Returns structured, predictable output
- Handles all error cases gracefully

**Estimated Time:** 3 hours

---

### Task 7.2: Create Test Suite

**Goal:** Comprehensive testing of OCR pipeline

**File to create:** `computer_vision/tests/test_ocr_pipeline.py`

**Steps:**

- [ ] Create automated test script:
  - Test directory of images
  - Expected results file (JSON mapping image → student_id)
  - Run pipeline on each image
  - Compare actual vs expected
  - Calculate accuracy metrics

- [ ] Test metrics to measure:
  - **Detection Rate:** % of images where card was detected
  - **Extraction Rate:** % of detected cards where ID was extracted
  - **Accuracy Rate:** % of extracted IDs that match expected
  - **Overall Success Rate:** End-to-end success
  - **Average Processing Time:** Mean time per card
  - **Confidence Distribution:** Histogram of confidence scores

- [ ] Create test report template:

  ```
  ===== OCR Pipeline Test Report =====
  Total Images Tested: X
  Cards Detected: X (XX%)
  IDs Extracted: X (XX%)
  Correct Extractions: X (XX%)
  Overall Success Rate: XX%
  Average Time: XXX ms
  Average Confidence: XX%

  Failed Cases:
  - image1.jpg: Card not detected
  - image2.jpg: OCR failed
  - image3.jpg: Wrong ID extracted (expected: XXX, got: YYY)
  ```

**Success Criteria:**

- Test suite runs automatically
- Generates detailed report
- Identifies failure patterns

**Estimated Time:** 3 hours

---

### Task 7.3: Benchmark and Optimize

**Goal:** Meet performance targets

**Target Metrics:**

- Detection rate: **> 95%**
- Extraction accuracy: **> 90%**
- Processing time: **< 1 second per card**

**Steps:**

- [ ] Run comprehensive test on 50+ cards
- [ ] Analyze results:
  - Which cards fail? Why?
  - Which preprocessing works best?
  - Which Tesseract config is optimal?

- [ ] Optimization strategies:
  - **If detection failing:**
    - Adjust Canny thresholds
    - Adjust area/aspect ratio filters
    - Add morphological operations
  - **If OCR failing:**
    - Try different preprocessing
    - Adjust binarization thresholds
    - Try different Tesseract PSM modes
    - Expand character whitelist
  - **If too slow:**
    - Reduce image resolution
    - Process only necessary ROI
    - Skip unnecessary preprocessing steps
    - Cache preprocessing results

- [ ] Iterate until targets are met
- [ ] Document final configuration

**Success Criteria:** Meet all performance targets

**Estimated Time:** 4 hours

---

## Phase 8: Error Handling & Robustness

### Task 8.1: Implement Comprehensive Error Handling

**Goal:** Handle all failure modes gracefully

**Steps:**

- [ ] Update `computer_vision/core/exceptions.py` with:
  - `CardNotFoundError`: No card in image
  - `CardDetectionAmbiguousError`: Multiple cards detected
  - `PerspectiveCorrectionError`: Invalid transformation
  - `OCRExtractionError`: Failed to extract student ID
  - `InvalidStudentIDError`: Extracted ID fails validation

- [ ] Add error handling to each module:
  - Wrap OpenCV operations in try-except
  - Validate inputs (None checks, type checks)
  - Validate outputs (reasonable dimensions, non-empty results)

- [ ] Create error recovery strategies:
  - If card detection fails: suggest better positioning
  - If OCR fails on first attempt: try alternative preprocessing
  - If extracted ID is invalid: flag for manual review

**Success Criteria:**

- System never crashes on bad input
- Clear error messages for all failure modes
- Logging provides debugging information

**Estimated Time:** 2 hours

---

### Task 8.2: Test Edge Cases

**Goal:** Ensure robustness to unusual inputs

**Test Cases:**

- [ ] No card in image
- [ ] Multiple cards in image
- [ ] Card partially outside frame
- [ ] Extremely poor lighting (very dark/bright)
- [ ] Blurry images
- [ ] Damaged/worn cards
- [ ] Cards with stickers or annotations
- [ ] Empty image / None input
- [ ] Wrong image format (not BGR)
- [ ] Very small images (< 100x100)
- [ ] Rotated 90°, 180°, 270°

**Success Criteria:** All edge cases handled without crashes

**Estimated Time:** 2 hours

---

## Phase 9: Integration with Main System

### Task 9.1: Create Public API

**Goal:** Simple interface for main system to use OCR module

**File to update:** `computer_vision/__init__.py`

**Steps:**

- [ ] Export main pipeline:

  ```python
  from computer_vision.pipeline.ocr_pipeline import CardOCRPipeline

  # Convenience function
  def scan_student_id_card(image: np.ndarray,
                           config: Dict = None) -> Dict:
      \"\"\"
      Scan student ID card and extract student ID

      Args:
          image: Camera captured image (BGR format)
          config: Optional configuration overrides

      Returns:
          {
              'success': bool,
              'student_id': str or None,
              'confidence': float,
              'error': str or None
          }
      \"\"\"
      pipeline = CardOCRPipeline(config or DEFAULT_CONFIG)
      return pipeline.scan_card(image)
  ```

- [ ] Create usage examples in `examples/basic_usage.py`
- [ ] Document API in `docs/ocr_api_reference.md`

**Success Criteria:** Main system can use OCR with single function call

**Estimated Time:** 2 hours

---

### Task 9.2: Database Integration

**Goal:** Store OCR results and maintain card-to-slot mapping

**Steps:**

- [ ] Define database schema for card mapping:

  ```sql
  CREATE TABLE card_inventory (
      id INTEGER PRIMARY KEY,
      student_id TEXT NOT NULL UNIQUE,
      slot_index INTEGER NOT NULL UNIQUE,
      scan_timestamp DATETIME,
      scan_confidence REAL,
      card_status TEXT  -- 'stored', 'dispensed', 'rejected'
  );
  ```

- [ ] Create functions to:
  - Store scan result: `store_card_scan(student_id, slot_index, confidence)`
  - Verify card match: `verify_card(expected_id, scanned_id) -> bool`
  - Update card status: `mark_card_dispensed(student_id)`

- [ ] Add transaction logging:

  ```sql
  CREATE TABLE scan_log (
      id INTEGER PRIMARY KEY,
      timestamp DATETIME,
      student_id TEXT,
      success BOOLEAN,
      confidence REAL,
      error_message TEXT,
      processing_time_ms REAL
  );
  ```

**Success Criteria:** OCR results persist to database

**Estimated Time:** 2 hours

---

## Phase 10: Documentation & Deployment

### Task 10.1: Write User Documentation

**Goal:** Complete documentation for system operators

**Documents to create:**

**1. Setup Guide** (`docs/ocr_setup_guide.md`)

- [ ] Installation instructions
- [ ] Camera positioning requirements
- [ ] Lighting setup recommendations
- [ ] Configuration file explanations
- [ ] Troubleshooting common issues

**2. API Reference** (`docs/ocr_api_reference.md`)

- [ ] All public functions with signatures
- [ ] Parameter descriptions
- [ ] Return value specifications
- [ ] Usage examples
- [ ] Error handling guide

**3. Maintenance Guide** (`docs/ocr_maintenance.md`)

- [ ] How to update ROI coordinates for new card designs
- [ ] How to retrain for different fonts
- [ ] Performance monitoring
- [ ] Log analysis

**Success Criteria:** Complete, clear documentation

**Estimated Time:** 4 hours

---

### Task 10.2: Create Calibration Tool

**Goal:** Easy way to adjust ROI coordinates for different card layouts

**File to create:** `computer_vision/tools/roi_calibrator.py`

**Steps:**

- [ ] Create interactive tool:
  - Load sample card image
  - Display card
  - Allow user to draw rectangles for ROI regions
  - Export ROI coordinates to config file

- [ ] Add validation:
  - Show extracted ROI preview
  - Test OCR on extracted ROI
  - Verify student ID is detected

**Success Criteria:** Non-technical user can calibrate ROI

**Estimated Time:** 3 hours

---

### Task 10.3: Final System Validation

**Goal:** End-to-end testing with real hardware

**Steps:**

- [ ] Set up camera in kiosk
- [ ] Test with 100+ real cards
- [ ] Measure performance:
  - Detection rate
  - Accuracy rate
  - Processing time
  - Error rate

- [ ] Stress testing:
  - Continuous operation for 1 hour
  - Process 50 cards back-to-back
  - Test under different lighting (morning, afternoon, evening)
  - Test after Raspberry Pi reboot

- [ ] Security testing:
  - Try with photocopies (should fail or warn)
  - Try with printed photos of cards
  - Try with expired cards from different years

- [ ] Document results in `docs/validation_report.md`

**Success Criteria:** System meets all operational requirements

**Estimated Time:** 4 hours

---

## Configuration Reference

### Key Configuration Parameters

**`config/ocr_config.py`**

```python
# Card Detection
CARD_DETECTION = {
    'min_area': 10000,
    'max_area': 500000,
    'aspect_ratio': 1.586,
    'aspect_ratio_tolerance': 0.3,
    'canny_threshold1': 50,
    'canny_threshold2': 150,
}

# Perspective Correction
CARD_OUTPUT_SIZE = (856, 539)  # Width x Height in pixels

# ROI Extraction (as fraction of card dimensions)
ROIS = {
    'student_id': {
        'x_start': 0.10,
        'x_end': 0.90,
        'y_start': 0.30,
        'y_end': 0.45,
    },
    'name': {
        'x_start': 0.10,
        'x_end': 0.90,
        'y_start': 0.50,
        'y_end': 0.65,
    }
}

# OCR Settings
TESSERACT_CONFIG = {
    'psm': 6,  # Page segmentation mode
    'oem': 3,  # OCR engine mode
    'char_whitelist': '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-/',
}

# Student ID Validation
STUDENT_ID_PATTERN = r'\\d{4}-\\d{2}-\\d{5}'  # Adjust to your format
VALID_YEAR_RANGE = (2015, 2030)

# Performance
MAX_RETRIES = 3
PROCESSING_TIMEOUT_MS = 2000
```

---

## Performance Targets

| Metric                 | Target  | Acceptable | Needs Improvement |
| ---------------------- | ------- | ---------- | ----------------- |
| Card Detection Rate    | > 98%   | > 95%      | < 95%             |
| ID Extraction Accuracy | > 95%   | > 90%      | < 90%             |
| Processing Time        | < 800ms | < 1200ms   | > 1200ms          |
| False Positive Rate    | < 1%    | < 2%       | > 2%              |
| System Uptime          | > 99%   | > 95%      | < 95%             |

---

## Troubleshooting Guide

### Problem: Card not detected

**Possible causes:**

- Card too far from camera
- Poor lighting (too dark or too bright)
- Card outside camera frame
- Reflective card surface causing glare

**Solutions:**

- Adjust camera position/distance
- Improve lighting setup (diffuse, even lighting)
- Add lighting guidelines in user instructions
- Adjust Canny edge detection thresholds
- Use polarizing filter on camera to reduce glare

---

### Problem: OCR extracts wrong student ID

**Possible causes:**

- Poor image quality (blurry, low resolution)
- Font not well-recognized by Tesseract
- Incorrect ROI coordinates
- Damaged card text

**Solutions:**

- Increase camera resolution
- Improve preprocessing (better binarization)
- Try different Tesseract PSM modes
- Train custom Tesseract model for your specific font
- Recalibrate ROI coordinates
- Implement checksum validation to catch errors

---

### Problem: Processing is too slow (> 1 second)

**Possible causes:**

- High resolution images
- Too many preprocessing steps
- Inefficient contour detection

**Solutions:**

- Reduce input image resolution (resize before processing)
- Process only ROI region for OCR (skip full image)
- Optimize preprocessing pipeline (remove unnecessary steps)
- Use threading (separate detection and OCR)
- Cache preprocessed images if multiple operations needed

---

### Problem: Extracting text from wrong region

**Possible causes:**

- ROI coordinates incorrect
- Card layout changed (new card design)
- Perspective correction failed

**Solutions:**

- Use ROI calibration tool to reconfigure
- Review card layout documentation
- Test perspective correction output
- Add visual debugging (save intermediate images)

---

## Progress Tracking

**Week 1:** Phases 1-2 (Setup, Card Detection)  
**Week 2:** Phases 3-5 (Perspective, ROI, Preprocessing)  
**Week 3:** Phases 6-7 (OCR Implementation, Integration)  
**Week 4:** Phases 8-10 (Error Handling, Testing, Documentation)

---

## Success Checklist

### Minimum Viable Product (MVP)

- [ ] Camera captures images successfully
- [ ] Card detection works (> 90% rate)
- [ ] Perspective correction produces straight cards
- [ ] ROI extraction isolates student ID region
- [ ] OCR extracts student ID (> 85% accuracy)
- [ ] Basic error handling implemented
- [ ] Simple API for main system

### Production-Ready System

- [ ] All MVP requirements met
- [ ] Card detection rate > 95%
- [ ] OCR accuracy > 90%
- [ ] Processing time < 1 second
- [ ] Comprehensive error handling
- [ ] Database integration complete
- [ ] Full documentation written
- [ ] System validated with real hardware
- [ ] Edge cases handled

### Enhanced System (Optional)

- [ ] OCR accuracy > 95%
- [ ] Multi-field extraction (name, program, year)
- [ ] Automatic font detection and adaptation
- [ ] Real-time preview for debugging
- [ ] Admin dashboard with statistics
- [ ] Automatic retraining based on failures

---

## Notes and Best Practices

1. **Test Early, Test Often**
   - Don't wait until the end to test integration
   - Create test images for each development stage
   - Keep a separate set of validation images (don't overtrain on test set)

2. **Document as You Go**
   - Keep notes on what works and what doesn't
   - Record all configuration changes
   - Take screenshots of successful results

3. **Start Simple, Iterate**
   - Get basic OCR working first
   - Add complexity gradually
   - Each addition should improve accuracy measurably

4. **Lighting is Critical**
   - Good lighting can compensate for mediocre algorithms
   - Bad lighting makes even the best algorithms fail
   - Invest time in proper lighting setup

5. **Tesseract Tuning**
   - PSM (Page Segmentation Mode) has huge impact on accuracy
   - Try all PSM modes 3, 6, 7, 11 and compare results
   - Character whitelist is very effective for structured text

6. **ROI Precision Matters**
   - Even 5% miscalibration can significantly hurt accuracy
   - Use the calibration tool
   - Test ROI on multiple card samples

7. **Version Control**
   - Commit after each working phase
   - Tag releases (v1.0-mvp, v2.0-production)
   - Keep old configurations in case you need to rollback

8. **Performance vs. Accuracy Trade-off**
   - More preprocessing usually means better accuracy but slower processing
   - Find the sweet spot for your requirements
   - Consider retry logic only for failed cases

---

## Recommended Development Order

1. ✅ Environment setup (Phase 1)
2. ✅ Card detection (Phase 2)
3. ✅ Perspective correction (Phase 3)
4. ✅ ROI extraction (Phase 4)
5. ✅ Preprocessing (Phase 5)
6. ✅ Basic OCR (Phase 6.1)
7. ✅ Student ID extraction (Phase 6.2)
8. ✅ Complete pipeline (Phase 7.1)
9. ✅ Testing and optimization (Phase 7.2-7.3)
10. ✅ Error handling (Phase 8)
11. ✅ Integration (Phase 9)
12. ✅ Documentation (Phase 10)

---

**Remember:** The goal is a reliable, maintainable system. Prioritize robustness over perfection. Good enough to work 95% of the time is better than perfect 80% of the time.

Good luck with your implementation!
