"""
OCR Configuration for Student ID Card System
Based on physical measurements from docs/card_layout.md
University of Dar es Salaam - 2022 Edition Cards
"""

# Card Physical Specifications
CARD_PHYSICAL = {
    'width_mm': 88,
    'height_mm': 55,
    'standard': 'CR80',  # Close to CR80 standard (85.60×53.98mm)
}

# Standard output size for perspective-corrected cards
# Maintains aspect ratio: 88/55 = 1.6
# Resolution: 10 pixels per mm
CARD_OUTPUT_SIZE = (880, 550)  # Width × Height in pixels

# Region of Interest Definitions
# Coordinates as percentage of card width/height (0.0 to 1.0)
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

# Anchor-based ROI detection (optional)
# Uses a detected anchor label (e.g., "NAME") and applies offsets
# Offsets are fractions of card width/height relative to anchor top-left.
ANCHOR_OCR = {
    'anchor_texts': ['NAME'],  # Update to the exact printed label on your card
    'min_confidence': 50,
    'psm': 6,
    'oem': 3,
    'char_whitelist': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ: ',
}

# Offsets relative to anchor top-left (fractions of card width/height)
# These are derived from your fixed ROIs assuming anchor aligns with the name line.
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

# Student ID Validation Rules
STUDENT_ID_PATTERN = r'\d{4}-\d{2}-\d{5}'  # Format: 2022-04-07227
VALID_YEAR_RANGE = (2015, 2030)
ID_TOTAL_LENGTH = 13  # Including hyphens

# Card Detection Parameters
CARD_DETECTION = {
    'min_area': 10000,           # Minimum contour area in pixels
    'max_area': 5000000,         # Maximum contour area in pixels (increased for high-res images)
    'aspect_ratio': 1.6,         # Expected aspect ratio (88/55)
    'aspect_ratio_tolerance': 1.0,  # Allowed deviation (increased for detection)
    'canny_threshold1': 30,      # Lower threshold for Canny edge detection (lowered)
    'canny_threshold2': 100,     # Upper threshold for Canny edge detection (lowered)
}

# OCR Settings (Tesseract)
TESSERACT_CONFIG = {
    'psm': 6,  # Page Segmentation Mode: Assume uniform block of text
    'oem': 3,  # OCR Engine Mode: Default (LSTM + Legacy)
    'char_whitelist': '0123456789-',  # Only digits and hyphens for student ID
}

# Build complete Tesseract config string
TESSERACT_CONFIG_STRING = (
    f"--psm {TESSERACT_CONFIG['psm']} "
    f"--oem {TESSERACT_CONFIG['oem']} "
    f"-c tessedit_char_whitelist={TESSERACT_CONFIG['char_whitelist']}"
)

# Font Properties (for reference)
FONT_PROPERTIES = {
    'name': 'Calibri',
    'size_pt': 9,
    'style': 'Bold',
    'color': 'Blue',  # Text color (may need color-specific preprocessing)
}

# Preprocessing Parameters
PREPROCESSING = {
    'denoise_strength': 10,           # fastNlMeansDenoising strength
    'clahe_clip_limit': 2.0,          # CLAHE contrast limit
    'clahe_tile_grid_size': (8, 8),   # CLAHE tile size
    'gaussian_blur_kernel': (5, 5),   # Gaussian blur kernel size
    'binary_threshold_blocksize': 11, # Adaptive threshold block size
    'binary_threshold_c': 2,          # Adaptive threshold constant
}

# Performance Settings
MAX_RETRIES = 3                  # Maximum OCR retry attempts
PROCESSING_TIMEOUT_MS = 2000     # Maximum processing time per card
CONFIDENCE_THRESHOLD = 0.7       # Minimum confidence score to accept result

# Known Challenges (for reference)
CHALLENGES = [
    'Low contrast text (blue on white)',
    'Glossy surface causing glare',
    'Background watermark interference',
    'Colored text (not black)',
    'Card edge wear',
    'Multiple text regions close together',
]

# Debug Settings
DEBUG = {
    'save_intermediate_images': False,  # Save preprocessing steps
    'debug_output_dir': 'data/debug_outputs',
    'verbose_logging': False,
}
