# Student ID Card Layout Documentation

**Purpose:** Document the physical and logical layout of your university's student ID cards to guide OCR implementation.

**Card Type/Version:** University of Dar es Salaam - from 2022 Editions  
**Measured By:** Samuel Dan Musyani

---

## 1. Physical Card Specifications

### Card Dimensions

- **Width:** 88 mm
- **Height:** 55 mm
- **Standard:** CR80 (Almost this standard)
- **Thickness:** 1 mm

### Card Material

- Material: PVC
- Surface finish: Glossy
- Color: Whitish background

### Printing Quality

- Print quality: Fair
- Text clarity: Low contrast
- Any visible wear on sample cards? Yes

---

## 2. Student ID Field Specification

This is the **PRIMARY** field your OCR system must extract.

### Location on Card

From **top-left corner** of the card:

- **Distance from left edge:** 1.5 mm
- **Distance from top edge:** 29 mm
- **Width of ID field:** 23 mm
- **Height of ID field:** 3.5 mm

### ID Format

- **Exact format pattern:** 2020-04-12345
- **Regex pattern:** `r'\d{4}-\d{2}-\d{5}'`
- **Total characters:** 13 (including separators)
- **Numeric only?** Yes (with hyphens)
- **Special characters:** Hyphens

### Sample Valid IDs

```bash
- 2022-04-07227
- 2022-04-11472
- 2022-04-09050
```

### ID Field Properties

- **Font name:** Calibri
- **Font size:** 9 pt
- **Font style:** Bold
- **Text color:** Blue
- **Background color/pattern:** Whitish
- **Text orientation:** Horizontal
- **Fixed-width font?** Yes

---

## 3. Additional Text Fields (Secondary)

### Field 1: Student Name

- **Location:** 1.5 mm from left, 21 mm from top, 57mm width, 4 mm height
- **Format:** Structured (`last_name, first_name middle_name`)
- **Font:** Calibri, Size: 9 pt, Color: Blue, Type: Bold
- **Purpose in system:** Display

### Field 2: Program/Major

- **Location:** 1.5 mm from left, 37 mm from top, 57 mm width, 4 mm height
- **Format:** B.Sc. in `Course name` (Electronics Engineering, Telecommunication Engineering)
- **Font:** Calibri, Size: 9 pt, Color: Red, Type: Blue
- **Purpose in system:** Display

### Field 3: Card Expiry Date

- **Location:** 18 mm from left, 40 mm from top, 21 mm width, 4 mm height
- **Format:** "DD/MM/YYYY"
- **Font:** Calibri, Size: 9 pt, Color: Red, Type: Bold
- **Purpose in system:** Validation

---

## 4. ROI (Region of Interest) Coordinates

These will be used to extract specific text regions during OCR.

**Calculation method:** Coordinates as **percentage** of card width/height (0.0 to 1.0).

### Primary ROI: Student ID Region

```python
STUDENT_ID_ROI = {
    'x_start': 0.017,  # % from left edge (1.5mm / 88mm)
    'x_end': 0.278,    # % from left edge (24.5mm / 88mm)
    'y_start': 0.527,  # % from top edge (29mm / 55mm)
    'y_end': 0.591,    # % from top edge (32.5mm / 55mm)
}
```

**Calculation:**

- Student ID at 1.5mm from left, 29mm from top
- Field dimensions: 23mm × 3.5mm
- x_start = 1.5 / 88 ≈ 0.017
- x_end = (1.5 + 23) / 88 = 24.5 / 88 ≈ 0.278
- y_start = 29 / 55 ≈ 0.527
- y_end = (29 + 3.5) / 55 = 32.5 / 55 ≈ 0.591

### Secondary ROI: Other Fields (if needed)

```python
NAME_ROI = {
    'x_start': 0.017,  # (1.5mm / 88mm)
    'x_end': 0.665,    # (58.5mm / 88mm)
    'y_start': 0.382,  # (21mm / 55mm)
    'y_end': 0.455,    # (25mm / 55mm)
}

PROGRAM_ROI = {
    'x_start': 0.017,  # (1.5mm / 88mm)
    'x_end': 0.665,    # (58.5mm / 88mm)
    'y_start': 0.673,  # (37mm / 55mm)
    'y_end': 0.745,    # (41mm / 55mm)
}

EXPIRY_DATE_ROI = {
    'x_start': 0.205,  # (18mm / 88mm)
    'x_end': 0.443,    # (39mm / 88mm)
    'y_start': 0.727,  # (40mm / 55mm)
    'y_end': 0.800,    # (44mm / 55mm)
}
```

---

## 5. Challenges and Special Considerations

### Text Recognition Challenges

- [x] Low contrast text
- [x] Reflective/glossy surface causes glare
- [x] Background pattern/watermark interferes with OCR
- [ ] Font is unusual or ornamental
- [ ] Text is very small
- [x] Colored text (not black)

### Positioning Challenges

- [ ] ID field location varies between card batches
- [ ] Card might be slightly rotated when inserted
- [x] Multiple text regions close together

### Environmental Challenges

- [ ] Card might have stickers/tape on it
- [x] Card edges are worn
- [ ] Card is laminated/sealed

---

## 7. Reference Images

### High-Quality Reference Card

- Save a clean, well-lit photo: `data/test_cards/reference.jpg`
- Annotate with ROI coordinates if possible: `data/test_results/reference_annotated.jpg`
- Include measurements marked on image

### Multiple Sample Cards

Create a directory with diverse examples:

```bash
data/test_cards/
  ├── reference_card_front.jpg          (high quality, well-lit)
  ├── sample_card_01.jpg                 (typical condition)
  ├── sample_card_02.jpg
  ├── sample_card_challenging_01.jpg    (poor lighting)
  └── sample_card_challenging_02.jpg    (damaged/worn)
```

---

## 8. Configuration Template

Once you've documented above, use this template for `config/ocr_config.py`:

```python
# Card Layout Configuration
# Based on physical measurements from card_layout.md
# University of Dar es Salaam - 2022 Edition Cards

CARD_PHYSICAL = {
    'width_mm': 88,
    'height_mm': 55,
    'standard': 'CR80',  # Close to CR80 standard (85.60×53.98mm)
}

# Standard output size for perspective-corrected cards
# Maintains aspect ratio: 88/55 = 1.6
CARD_OUTPUT_SIZE = (880, 550)  # Width × Height in pixels (10px per mm)

ROIS = {
    'student_id': {
        'x_start': 0.017,  # % from left
        'x_end': 0.278,
        'y_start': 0.527,  # % from top
        'y_end': 0.591,
    },
    'name': {
        'x_start': 0.017,
        'x_end': 0.665,
        'y_start': 0.382,
        'y_end': 0.455,
    },
    'program': {
        'x_start': 0.017,
        'x_end': 0.665,
        'y_start': 0.673,
        'y_end': 0.745,
    },
    'expiry_date': {
        'x_start': 0.205,
        'x_end': 0.443,
        'y_start': 0.727,
        'y_end': 0.800,
    }
}

# Student ID Validation
STUDENT_ID_PATTERN = r'\d{4}-\d{2}-\d{5}'  # Format: 2022-04-07227
VALID_YEAR_RANGE = (2015, 2030)
ID_TOTAL_LENGTH = 13  # Including hyphens

# OCR Settings
TESSERACT_CONFIG = {
    'psm': 6,  # Assume uniform block of text
    'oem': 3,  # Default OCR Engine Mode
    'char_whitelist': '0123456789-',  # Only digits and hyphens for ID
}

# Font Properties (for reference)
FONT_PROPERTIES = {
    'name': 'Calibri',
    'size_pt': 9,
    'style': 'Bold',
    'color': 'Blue',  # Text color (may need color-specific preprocessing)
}

# Known Challenges
CHALLENGES = [
    'Low contrast text (blue on white)',
    'Glossy surface causing glare',
    'Background watermark interference',
    'Colored text (not black)',
    'Card edge wear',
    'Multiple text regions close together',
]
```

---

## 9. Measurement Checklist

Before proceeding to Phase 2, verify you have:

- [x] Physical card dimensions documented
- [x] Student ID format with regex pattern defined
- [x] Student ID location measured (from top-left corner)
- [x] Student ID font properties recorded
- [x] ROI percentages calculated
- [x] At least one reference card image saved
- [ ] At least 5 sample cards photographed at various angles
- [x] All challenges/variations listed
- [ ] Card layout diagram or annotated image created

---
