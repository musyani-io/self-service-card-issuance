import cv2
import numpy as np
from typing import Optional

def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Converts color image to grayscale

    A grayscale is one brightness channel, while color is 3 channels.
    Parameters:
        image(np.ndarray): Color image with shape(height, width, 3)
    Returns:
        np.ndarray: Grayscale image with shape(height, width)
    Raises:
        ValueError: If image is None or not a valid NumPy array
        ValueError: If image is not a color image (3 channels)
    """

    # Check presence
    if image is None:
        raise ValueError("Image cannot be None. Please provide the image")
    
    # Checks type
    if not isinstance(image, np.ndarray):
        raise ValueError(f"Image must be a NumPy array. Received type: {str(type(image))}")
    
    # Checks for a color image
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError(f"Image must have 3 channels. Received shape: {image.shape}")
    
    # Grayscale conversion
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return gray_image