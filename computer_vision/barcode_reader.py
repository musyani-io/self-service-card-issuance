"""
Barcode detection and decoding module.

Handles locating barcodes in images and extracting student ID information.
Uses pyzbar library for robust barcode detection and decoding.
"""

import numpy as np
from typing import Optional, List, Dict, Tuple
from pyzbar import pyzbar
import cv2


def detect_barcode_location(image: np.ndarray) -> Optional[Dict]:
    """
    Detect barcode location in image using pyzbar.
    
    This function locates barcodes in the image and returns the bounding box
    coordinates. It uses pyzbar which supports multiple barcode types including
    Code128, Code39, QR codes, and more.
    
    Args:
        image: Input image (color or grayscale numpy array)
        
    Returns:
        Dictionary with barcode location info:
        {
            'bbox': (x, y, width, height),  # Bounding box coordinates
            'type': str,                     # Barcode type (e.g., 'CODE128')
            'polygon': [(x1,y1), (x2,y2)...],# Corner points of barcode region
            'quality': int,                  # Quality score (0-100, if available)
        }
        Returns None if no barcode is found.
        
    Raises:
        ValueError: If image is None or empty
        
    Example:
        >>> image = cv2.imread('id_card.jpg')
        >>> result = detect_barcode_location(image)
        >>> if result:
        ...     x, y, w, h = result['bbox']
        ...     print(f"Barcode found at ({x}, {y}), size: {w}x{h}")
    """
    if image is None or image.size == 0:
        raise ValueError("Input image is None or empty")
    
    # pyzbar works with grayscale or color images
    # Detect barcodes using pyzbar
    detected_barcodes = pyzbar.decode(image)
    
    # Return None if no barcodes found
    if not detected_barcodes:
        return None
    
    # Get the first detected barcode (handle multiple barcodes later)
    barcode = detected_barcodes[0]
    
    # Extract bounding box (pyzbar returns a Rect object)
    x, y, w, h = barcode.rect.left, barcode.rect.top, barcode.rect.width, barcode.rect.height
    
    # Extract polygon points (corner points of barcode region)
    polygon = [(point.x, point.y) for point in barcode.polygon]
    
    # Calculate quality score (based on polygon area vs bbox area)
    # A perfect rectangle has ratio close to 1.0
    bbox_area = w * h
    if len(polygon) >= 3:
        # Calculate polygon area using Shoelace formula
        polygon_area = 0.5 * abs(sum(polygon[i][0] * polygon[(i+1) % len(polygon)][1] 
                                     - polygon[(i+1) % len(polygon)][0] * polygon[i][1]
                                     for i in range(len(polygon))))
        quality = int(min(100, (polygon_area / bbox_area) * 100)) if bbox_area > 0 else 0
    else:
        quality = 50  # Default quality if polygon is incomplete
    
    return {
        'bbox': (x, y, w, h),
        'type': barcode.type,
        'polygon': polygon,
        'quality': quality,
    }


def detect_all_barcodes(image: np.ndarray) -> List[Dict]:
    """
    Detect all barcodes in an image.
    
    Some ID cards may have multiple barcodes (front/back codes, multiple formats).
    This function returns information for all detected barcodes.
    
    Args:
        image: Input image (color or grayscale numpy array)
        
    Returns:
        List of dictionaries, each containing:
        {
            'bbox': (x, y, width, height),
            'type': str,
            'polygon': [(x1,y1), (x2,y2)...],
            'quality': int,
        }
        Returns empty list if no barcodes found.
        
    Raises:
        ValueError: If image is None or empty
        
    Example:
        >>> image = cv2.imread('card.jpg')
        >>> barcodes = detect_all_barcodes(image)
        >>> print(f"Found {len(barcodes)} barcode(s)")
    """
    if image is None or image.size == 0:
        raise ValueError("Input image is None or empty")
    
    detected_barcodes = pyzbar.decode(image)
    
    results = []
    for barcode in detected_barcodes:
        x, y, w, h = barcode.rect.left, barcode.rect.top, barcode.rect.width, barcode.rect.height
        polygon = [(point.x, point.y) for point in barcode.polygon]
        
        # Calculate quality
        bbox_area = w * h
        if len(polygon) >= 3:
            polygon_area = 0.5 * abs(sum(polygon[i][0] * polygon[(i+1) % len(polygon)][1] 
                                         - polygon[(i+1) % len(polygon)][0] * polygon[i][1]
                                         for i in range(len(polygon))))
            quality = int(min(100, (polygon_area / bbox_area) * 100)) if bbox_area > 0 else 0
        else:
            quality = 50
        
        results.append({
            'bbox': (x, y, w, h),
            'type': barcode.type,
            'polygon': polygon,
            'quality': quality,
        })
    
    return results


def get_barcode_confidence(image: np.ndarray, bbox: Tuple[int, int, int, int]) -> float:
    """
    Calculate confidence score for detected barcode region.
    
    Analyzes the barcode region to determine detection confidence based on:
    - Edge density in the region (barcodes have many vertical edges)
    - Contrast levels
    - Size appropriateness
    
    Args:
        image: Input image (grayscale recommended)
        bbox: Bounding box (x, y, width, height)
        
    Returns:
        Confidence score from 0.0 to 1.0
        - 1.0 = very confident this is a barcode
        - 0.0 = likely not a barcode
        
    Raises:
        ValueError: If image is None or bbox is invalid
        
    Example:
        >>> image = cv2.imread('card.jpg', cv2.IMREAD_GRAYSCALE)
        >>> bbox = (50, 200, 300, 80)
        >>> confidence = get_barcode_confidence(image, bbox)
        >>> if confidence > 0.7:
        ...     print("High confidence barcode detection")
    """
    if image is None or image.size == 0:
        raise ValueError("Input image is None or empty")
    
    x, y, w, h = bbox
    
    # Validate bbox
    if x < 0 or y < 0 or w <= 0 or h <= 0:
        raise ValueError(f"Invalid bounding box: {bbox}")
    
    # Ensure bbox is within image bounds
    img_h, img_w = image.shape[:2]
    if x + w > img_w or y + h > img_h:
        raise ValueError(f"Bounding box {bbox} exceeds image dimensions {img_w}x{img_h}")
    
    # Extract barcode region
    roi = image[y:y+h, x:x+w]
    
    # Convert to grayscale if needed
    if len(roi.shape) == 3:
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Factor 1: Edge density (barcodes have lots of vertical edges)
    # Use Sobel operator to find vertical edges
    sobel_x = cv2.Sobel(roi, cv2.CV_64F, 1, 0, ksize=3)
    edge_density = np.mean(np.abs(sobel_x))
    edge_score = min(1.0, edge_density / 50.0)  # Normalize
    
    # Factor 2: Contrast (barcodes have high contrast)
    contrast = np.std(roi)
    contrast_score = min(1.0, contrast / 64.0)  # Normalize
    
    # Factor 3: Size appropriateness (barcodes typically have specific aspect ratios)
    aspect_ratio = w / h if h > 0 else 0
    # Most barcodes are wider than tall (aspect ratio 2:1 to 10:1)
    if 2.0 <= aspect_ratio <= 10.0:
        size_score = 1.0
    elif 1.0 <= aspect_ratio < 2.0 or 10.0 < aspect_ratio <= 15.0:
        size_score = 0.7
    else:
        size_score = 0.3
    
    # Weighted combination
    confidence = (edge_score * 0.4 + contrast_score * 0.3 + size_score * 0.3)
    
    return round(confidence, 3)


# ============================================================================
# TASK 4.2: Barcode Decoding Functions
# ============================================================================

def decode_barcode(image: np.ndarray) -> Optional[str]:
    """
    Decode barcode data from an image using pyzbar library.
    
    Extracts the barcode string data from the first barcode found in the image.
    Attempts to decode using pyzbar's built-in barcode format detection.
    
    Args:
        image (np.ndarray): Input image in BGR, RGB, or grayscale format.
                           Assumed to be a 2D (grayscale) or 3D (color) array.
    
    Returns:
        Optional[str]: The decoded barcode data as a string, or None if no
                      barcode is found or decoding fails. Barcode data is
                      decoded from bytes to UTF-8 string.
    
    Raises:
        ValueError: If image is None, not a numpy array, or has invalid shape.
    
    Examples:
        >>> decoded_data = decode_barcode(image)
        >>> if decoded_data:
        >>>     print(f"Barcode found: {decoded_data}")
        >>> else:
        >>>     print("No barcode detected")
    
    Notes:
        - pyzbar attempts auto-detection of barcode format
        - Decodes data field from pyzbar result object
        - Handles bytes-to-string conversion automatically
        - Returns None gracefully if no barcodes detected (not an error)
        - Optimized for images pre-processed by the Phase 3 pipeline
    """
    # Input validation
    if image is None:
        raise ValueError("Image cannot be None")
    if not isinstance(image, np.ndarray):
        raise ValueError(f"Image must be numpy array, got {type(image)}")
    if image.size == 0:
        raise ValueError("Image array is empty")
    if len(image.shape) not in (2, 3):
        raise ValueError(f"Image must be 2D or 3D array, got shape {image.shape}")
    
    try:
        # Detect and decode barcodes using pyzbar
        decoded_objects = pyzbar.decode(image)
        
        # Return data from first barcode if found
        if decoded_objects:
            barcode_data = decoded_objects[0].data
            # Convert bytes to string (handle UTF-8 decoding)
            return barcode_data.decode('utf-8')
        
        # No barcode found - return None (not an error)
        return None
        
    except Exception as e:
        # Log unexpected errors but return None for graceful failure
        return None


def decode_barcode_from_region(image: np.ndarray, bbox: Dict) -> Optional[str]:
    """
    Decode barcode data from a specific region of interest (ROI) in an image.
    
    Uses the bbox coordinates from a prior detection step to crop the image
    and decode only that region. Useful for multi-barcode images where you
    want to decode a specific detected barcode.
    
    Args:
        image (np.ndarray): Input image in BGR, RGB, or grayscale format.
        bbox (Dict): Bounding box dictionary with keys:
                    - 'x': Left edge x-coordinate (int)
                    - 'y': Top edge y-coordinate (int)
                    - 'width': Bounding box width (int)
                    - 'height': Bounding box height (int)
    
    Returns:
        Optional[str]: The decoded barcode data as a string from the region,
                      or None if decoding fails or bbox is invalid.
    
    Raises:
        ValueError: If image is None/invalid, bbox is None, or bbox missing keys.
    
    Examples:
        >>> detection = detect_barcode_location(image)
        >>> if detection:
        >>>     decoded = decode_barcode_from_region(image, detection['bbox'])
        >>>     print(f"Decoded: {decoded}")
    
    Notes:
        - Validates bbox structure before processing
        - Gracefully handles out-of-bounds coordinates (clips to image bounds)
        - Returns None if bbox results in invalid region
        - Useful for multi-barcode scenarios to decode specific barcodes
    """
    # Input validation
    if image is None:
        raise ValueError("Image cannot be None")
    if not isinstance(image, np.ndarray):
        raise ValueError(f"Image must be numpy array, got {type(image)}")
    
    if bbox is None:
        raise ValueError("Bounding box cannot be None")
    if not isinstance(bbox, dict):
        raise ValueError(f"Bounding box must be dict, got {type(bbox)}")
    
    # Validate bbox contains required keys
    required_keys = {'x', 'y', 'width', 'height'}
    if not required_keys.issubset(bbox.keys()):
        missing = required_keys - bbox.keys()
        raise ValueError(f"Bounding box missing keys: {missing}")
    
    try:
        # Extract bbox coordinates
        x = int(bbox['x'])
        y = int(bbox['y'])
        width = int(bbox['width'])
        height = int(bbox['height'])
        
        # Validate coordinates are positive
        if x < 0 or y < 0 or width <= 0 or height <= 0:
            return None
        
        # Clip to image bounds
        h, w = image.shape[:2]
        x_end = min(x + width, w)
        y_end = min(y + height, h)
        
        # Skip if region would be invalid after clipping
        if x >= w or y >= h or x_end <= x or y_end <= y:
            return None
        
        # Crop ROI
        roi = image[y:y_end, x:x_end]
        
        # Return None if ROI is empty
        if roi.size == 0:
            return None
        
        # Decode from cropped region
        decoded_objects = pyzbar.decode(roi)
        if decoded_objects:
            return decoded_objects[0].data.decode('utf-8')
        
        return None
        
    except (KeyError, TypeError, ValueError):
        # Handle coordinate conversion or bbox format errors
        return None


def validate_barcode_format(barcode_data: Optional[str],
                           expected_format: Optional[str] = None) -> bool:
    """
    Validate barcode data matches expected format (if specified).
    
    Checks if decoded barcode data satisfies format requirements. Can validate
    against a specific expected format pattern (e.g., student ID, employee ID)
    or perform basic sanity checks if no format is specified.
    
    Args:
        barcode_data (Optional[str]): The decoded barcode data to validate.
                                      Can be None.
        expected_format (Optional[str]): Expected format pattern. Options:
                                        - None: Perform basic sanity checks
                                        - 'student_id': 10-digit format
                                        - 'employee_id': Custom format
                                        - Custom regex pattern as string
    
    Returns:
        bool: True if data is valid and matches format, False otherwise.
    
    Raises:
        ValueError: If expected_format is unrecognized (not None and invalid).
    
    Examples:
        >>> data = decode_barcode(image)
        >>> if validate_barcode_format(data, 'student_id'):
        >>>     print("Valid student ID barcode")
        >>> else:
        >>>     print("Invalid format")
    
    Notes:
        - Returns False if barcode_data is None (treat as invalid)
        - Returns False if barcode_data is empty string
        - Basic sanity: checks data is alphanumeric and 5-50 chars
        - Student ID format: exactly 10 digits
        - Employee ID format: 6-8 alphanumeric characters
        - Custom format: treated as regex pattern for flexible validation
        - Gracefully handles None inputs (returns False, not error)
    """
    # Gracefully handle None or empty data
    if barcode_data is None or not isinstance(barcode_data, str):
        return False
    
    if not barcode_data or len(barcode_data) == 0:
        return False
    
    # If no format specified, perform basic sanity checks
    if expected_format is None:
        # Basic checks: non-empty, reasonable length, alphanumeric
        if not (5 <= len(barcode_data) <= 50):
            return False
        if not barcode_data.replace('_', '').replace('-', '').isalnum():
            return False
        return True
    
    # Validate against specific format patterns
    if expected_format == 'student_id':
        # Student ID: exactly 10 digits
        if len(barcode_data) == 10 and barcode_data.isdigit():
            return True
        return False
    
    elif expected_format == 'employee_id':
        # Employee ID: 6-8 alphanumeric characters
        if 6 <= len(barcode_data) <= 8 and barcode_data.isalnum():
            return True
        return False
    
    elif expected_format == 'card_number':
        # Card number: typically 16-19 digits with optional hyphens/spaces
        clean_data = barcode_data.replace('-', '').replace(' ', '')
        if 16 <= len(clean_data) <= 19 and clean_data.isdigit():
            return True
        return False
    
    else:
        # Treat as custom regex pattern
        try:
            import re
            if re.match(expected_format, barcode_data):
                return True
            return False
        except re.error:
            # Invalid regex pattern
            raise ValueError(f"Invalid regex pattern: {expected_format}")


def handle_decode_error(image: np.ndarray,
                       error: str,
                       retry_config: Optional[Dict] = None) -> Dict:
    """
    Handle barcode decoding errors and suggest recovery strategies.
    
    When barcode decoding fails, analyzes the failure and returns diagnostic
    information and suggested recovery actions. Can recommend preprocessing
    adjustments to improve decodability.
    
    Args:
        image (np.ndarray): The image where decoding failed.
        error (str): Description of the error that occurred.
        retry_config (Optional[Dict]): Configuration for retry suggestions.
                                      Keys:
                                      - 'max_retries': Max retry attempts (default: 3)
                                      - 'preprocessing_steps': List of preprocessing
                                        functions to try (default: None)
    
    Returns:
        Dict: Diagnostic information with keys:
              - 'error': Original error message
              - 'image_shape': Image dimensions (height, width, channels)
              - 'image_stats': Basic image statistics (mean, std)
              - 'suggested_actions': List of recovery suggestions
              - 'retry_recommended': Boolean whether retry is advised
              - 'preprocessing_suggestions': List of preprocessing functions
                to try for image improvement
    
    Raises:
        ValueError: If image is None or invalid.
    
    Examples:
        >>> data = decode_barcode(image)
        >>> if data is None:
        >>>     error_info = handle_decode_error(image, "No barcode detected")
        >>>     print(f"Suggestions: {error_info['suggested_actions']}")
    
    Notes:
        - Analyzes image statistics to diagnose potential issues
        - Suggests preprocessing steps based on image characteristics
        - Useful for implementing retry logic with progressive improvements
        - Helps differentiate between image quality vs barcode presence issues
    """
    # Input validation
    if image is None:
        raise ValueError("Image cannot be None")
    if not isinstance(image, np.ndarray):
        raise ValueError(f"Image must be numpy array, got {type(image)}")
    
    # Set defaults for retry config
    if retry_config is None:
        retry_config = {}
    
    max_retries = retry_config.get('max_retries', 3)
    
    # Analyze image statistics
    h, w = image.shape[:2]
    channels = image.shape[2] if len(image.shape) == 3 else 1
    
    image_mean = float(np.mean(image))
    image_std = float(np.std(image))
    
    # Determine suggestions based on image characteristics
    suggested_actions = []
    preprocessing_suggestions = []
    
    # Too bright or too dark
    if image_mean > 200:
        suggested_actions.append("Image too bright - reduce exposure or enhance contrast")
        preprocessing_suggestions.append("enhance_contrast")
    elif image_mean < 50:
        suggested_actions.append("Image too dark - increase exposure")
        preprocessing_suggestions.append("enhance_contrast")
    
    # Low contrast (low std)
    if image_std < 15:
        suggested_actions.append("Low contrast - adjust lighting or apply contrast enhancement")
        preprocessing_suggestions.append("enhance_contrast")
    
    # High noise (high std)
    if image_std > 60:
        suggested_actions.append("High noise - apply blur/smoothing filters")
        preprocessing_suggestions.append("gaussian_blur")
    
    # Small image
    if h < 100 or w < 100:
        suggested_actions.append("Image too small - increase camera resolution or zoom")
    
    # Image orientation issue
    if h > w * 1.5:
        suggested_actions.append("Image portrait orientation - barcode may be rotated")
    
    # Default suggestions if no specific issues detected
    if not suggested_actions:
        suggested_actions.append("Ensure barcode is fully visible and in focus")
        suggested_actions.append("Check lighting - avoid glare or shadows")
        suggested_actions.append("Position barcode centered in frame")
        preprocessing_suggestions = ["gaussian_blur", "enhance_contrast"]
    
    # Build result dictionary
    return {
        'error': error,
        'image_shape': (h, w, channels),
        'image_stats': {
            'mean': round(image_mean, 2),
            'std': round(image_std, 2)
        },
        'suggested_actions': suggested_actions,
        'retry_recommended': max_retries > 0,
        'preprocessing_suggestions': preprocessing_suggestions
    }
