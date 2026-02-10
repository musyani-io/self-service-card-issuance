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

### Anchor-Based ROI (Final Offsets)

Anchor label: **NAME** (top-left of the anchor text box). Offsets are fractions of card width/height from the anchor top-left.

```python
ANCHOR_ROI_OFFSETS = {
    'name': {
        'dx': -0.008,
        'dy': 0.064,
        'w': 0.648,
        'h': 0.073,
    },
    'student_id': {
        'dx': -0.010,
        'dy': 0.203,
        'w': 0.261,
        'h': 0.086,
    },
    'program': {
        'dx': -0.013,
        'dy': 0.322,
        'w': 0.648,
        'h': 0.072,
    },
    'expiry_date': {
        'dx': 0.166,
        'dy': 0.394,
        'w': 0.238,
        'h': 0.073,
    },
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
- Annotate with anchor label if possible: `data/test_results/reference_annotated.jpg`
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

ANCHOR_OCR = {
    'anchor_texts': ['NAME'],  # Update to the exact printed label on your card
    'min_confidence': 50,
    'psm': 6,
    'oem': 3,
    'char_whitelist': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ: ',
}

# Offsets relative to anchor top-left (fractions of card width/height)
ANCHOR_ROI_OFFSETS = {
    'name': {
        'dx': 0.000,
        'dy': 0.000,
        'w': 0.648,
        'h': 0.073,
    },
    'student_id': {
        'dx': 0.000,
        'dy': 0.145,
        'w': 0.261,
        'h': 0.064,
    },
    'program': {
        'dx': 0.000,
        'dy': 0.291,
        'w': 0.648,
        'h': 0.072,
    },
    'expiry_date': {
        'dx': 0.188,
        'dy': 0.345,
        'w': 0.238,
        'h': 0.073,
    },
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
