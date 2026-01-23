"""
Image preprocessing utilities.

Provides functions for image enhancement, transformation, and preparation
for barcode detection.
"""

import cv2
import numpy as np
from typing import Tuple, Optional


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Convert a color image to grayscale.
    
    Grayscale conversion simplifies barcode detection by removing color information
    and focusing on intensity patterns, which is what barcode readers need.
    
    Args:
        image: Input image in BGR, RGB, RGBA, or already grayscale format
        
    Returns:
        Grayscale image as numpy array
        
    Raises:
        ValueError: If image is None or empty
    """
    if image is None or image.size == 0:
        raise ValueError("Input image is None or empty")
    
    # Check if already grayscale (2D array)
    if len(image.shape) == 2:
        return image
    
    # Determine number of channels
    channels = image.shape[2] if len(image.shape) == 3 else 1
    
    # Convert based on channel count
    if channels == 4:
        # RGBA or BGRA - convert to grayscale (alpha channel ignored)
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    elif channels == 3:
        # Assume BGR (OpenCV default) - most common case
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        # Single channel, already grayscale
        gray = image
    
    return gray


def resize_image(image: np.ndarray, target_width: int, maintain_aspect: bool = True, 
                 min_width: int = 150, max_shrink_ratio: float = 0.5) -> np.ndarray:
    """
    Resize image to a target width while optionally maintaining aspect ratio.
    
    Resizing reduces processing time and provides consistent dimensions for barcode detection.
    Smaller images process faster on Raspberry Pi; larger images preserve fine barcode details.
    
    Args:
        image: Input image (color or grayscale)
        target_width: Desired width in pixels
        maintain_aspect: If True, height scales proportionally; if False, image is stretched
        min_width: Minimum width allowed (prevents excessive shrinkage). Default 150px.
        max_shrink_ratio: Maximum shrinkage allowed as ratio (0.5 = don't shrink below 50% of original).
                         Default 0.5 (50% minimum). Range: 0.1 to 1.0.
        
    Returns:
        Resized image as numpy array
        
    Raises:
        ValueError: If image is None, empty, target_width is invalid, or shrinkage exceeds limits
    """
    if image is None or image.size == 0:
        raise ValueError("Input image is None or empty")
    
    if target_width <= 0:
        raise ValueError(f"target_width must be positive, got {target_width}")
    
    if not (0.1 <= max_shrink_ratio <= 1.0):
        raise ValueError(f"max_shrink_ratio must be between 0.1 and 1.0, got {max_shrink_ratio}")
    
    height, width = image.shape[:2]
    
    # Enforce minimum width
    if target_width < min_width:
        target_width = min_width
    
    # Enforce maximum shrinkage ratio
    min_allowed_width = int(width * max_shrink_ratio)
    if target_width < min_allowed_width:
        raise ValueError(
            f"Requested width {target_width}px exceeds max shrinkage. "
            f"Original width: {width}px, allowed minimum: {min_allowed_width}px "
            f"(max_shrink_ratio: {max_shrink_ratio})"
        )
    
    if maintain_aspect:
        # Calculate new height to maintain aspect ratio (width:height stays the same)
        aspect_ratio = height / width
        new_height = int(target_width * aspect_ratio)
        new_size = (target_width, new_height)
    else:
        # Stretch to exact dimensions (not recommended for barcodes)
        new_size = (target_width, height)
    
    # Use INTER_AREA for shrinking (better quality), INTER_LINEAR for enlarging
    if target_width < width:
        interpolation = cv2.INTER_AREA
    else:
        interpolation = cv2.INTER_LINEAR
    
    # Perform resize operation
    resized = cv2.resize(image, new_size, interpolation=interpolation)
    
    return resized


def crop_roi(image: np.ndarray, x: Optional[int] = None, y: Optional[int] = None, 
             width: Optional[int] = None, height: Optional[int] = None) -> np.ndarray:
    """
    Crop a region of interest (ROI) from an image.
    
    By default, crops the bottom half of the image (optimized for ID cards with barcode at bottom).
    This optional cropping improves detection quality by reducing noise and focusing on barcode area.
    For custom regions, provide x, y, width, height coordinates.
    
    Cropping focuses processing on the barcode area, reducing noise and improving detection speed.
    Useful when barcode location is known or predicted (e.g., always in bottom half of ID card).
    
    Args:
        image: Input image (color or grayscale)
        x: Top-left corner x-coordinate (column) - optional, defaults to full width (0)
        y: Top-left corner y-coordinate (row) - optional, defaults to image midpoint
        width: Width of the ROI in pixels - optional, defaults to full image width
        height: Height of the ROI in pixels - optional, defaults to bottom half height
        
    Returns:
        Cropped image as numpy array containing only the ROI (bottom half by default)
        
    Raises:
        ValueError: If image is None, empty, or ROI coordinates are invalid
    """
    if image is None or image.size == 0:
        raise ValueError("Input image is None or empty")
    
    img_height, img_width = image.shape[:2]
    
    # If no coordinates provided, default to bottom half (optimized for ID cards)
    if x is None or y is None or width is None or height is None:
        x = 0  # Start from left edge
        y = img_height // 2  # Start from midpoint (bottom half)
        width = img_width  # Full width
        height = img_height - y  # From midpoint to bottom
    
    # Validate coordinates
    if x < 0 or y < 0:
        raise ValueError(f"Coordinates must be non-negative: x={x}, y={y}")
    
    if width <= 0 or height <= 0:
        raise ValueError(f"Width and height must be positive: width={width}, height={height}")
    
    # Clip ROI to image boundaries to prevent out-of-bounds errors
    x_end = min(x + width, img_width)
    y_end = min(y + height, img_height)
    
    # Ensure ROI is within bounds
    if x >= img_width or y >= img_height:
        raise ValueError(
            f"ROI starting point ({x}, {y}) is outside image bounds ({img_width}, {img_height})"
        )
    
    # Crop using numpy array slicing: [rows (y), columns (x)]
    cropped = image[y:y_end, x:x_end]
    
    return cropped


def save_debug_image(image: np.ndarray, filepath: str, 
                     annotations: Optional[list] = None) -> None:
    """
    Save an image to disk with optional annotations for debugging.
    
    Useful for visually inspecting preprocessing results and barcode detection.
    Supports drawing bounding boxes and text labels on the image before saving.
    
    Args:
        image: Input image to save (color or grayscale)
        filepath: Full path where image should be saved (e.g., '/path/to/debug.jpg')
        annotations: Optional list of annotations to draw on image before saving.
                    Each annotation is a dict with:
                    - 'type': 'bbox' or 'text'
                    - 'bbox': (x, y, width, height) for bounding box
                    - 'text': string to display for text annotation
                    - 'position': (x, y) for text top-left corner
                    - 'color': (B, G, R) tuple, default (0, 255, 0) for bbox, (255, 0, 0) for text
                    - 'thickness': line thickness for bbox, default 2
    
    Returns:
        None
        
    Raises:
        ValueError: If image is None or empty
        IOError: If directory doesn't exist or file cannot be written
    """
    if image is None or image.size == 0:
        raise ValueError("Input image is None or empty")
    
    # Create output directory if it doesn't exist
    import os
    output_dir = os.path.dirname(filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Make a copy to avoid modifying original image
    debug_image = image.copy()
    
    # Convert grayscale to BGR for color annotations (if needed)
    if len(debug_image.shape) == 2:
        debug_image = cv2.cvtColor(debug_image, cv2.COLOR_GRAY2BGR)
    
    # Apply annotations if provided
    if annotations:
        for annotation in annotations:
            anno_type = annotation.get('type', 'bbox')
            
            if anno_type == 'bbox':
                # Draw bounding box rectangle
                x, y, w, h = annotation['bbox']
                color = annotation.get('color', (0, 255, 0))  # Default green
                thickness = annotation.get('thickness', 2)
                # Draw rectangle: top-left (x, y) to bottom-right (x+w, y+h)
                cv2.rectangle(debug_image, (x, y), (x + w, y + h), color, thickness)
            
            elif anno_type == 'text':
                # Draw text label
                text = annotation.get('text', '')
                x, y = annotation['position']
                color = annotation.get('color', (255, 0, 0))  # Default blue
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = annotation.get('font_scale', 0.5)
                thickness = annotation.get('thickness', 1)
                # Put text on image
                cv2.putText(debug_image, text, (x, y), font, font_scale, color, thickness)
    
    # Save image to file
    success = cv2.imwrite(filepath, debug_image)
    if not success:
        raise IOError(f"Failed to save image to {filepath}")


def apply_threshold(image, method='adaptive'):
    """
    Apply thresholding to enhance barcode contrast.
    
    Args:
        image: Input grayscale image
        method: Thresholding method ('adaptive', 'otsu', 'binary')
        
    Returns:
        Thresholded binary image
    """
    pass


def crop_region(image, roi):
    """
    Crop region of interest from image.
    
    Args:
        image: Input image
        roi: Region of interest coordinates (x, y, w, h)
        
    Returns:
        Cropped image
    """
    pass


def enhance_image(image):
    """
    Apply various enhancement techniques for better barcode detection.
    
    Args:
        image: Input image
        
    Returns:
        Enhanced image
    """
    pass
