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


def resize_image(image: np.ndarray, max_width: int = 640) -> np.ndarray:
    """
    Resize image while maintaining aspect ratio

    Parameters:
        image(np.ndarray): Input image
        max_width (int): Target width in pixels

    Returns:
        np.ndarray: Resized image with new shape (new_height, new_width(640))

    Raises:
        ValueError: If image is None, not NumPy array or max_width <= 0.
    """
    
    # If there's no image
    if image is None:
        raise ValueError("Image cannot be None")

    # Checks for NumPy type
    if not isinstance(image, np.ndarray):
        raise ValueError(f"Image must be NumPy array. Received: {type(image)}")
    
    # Extract original dimensions
    og_height, og_width = image.shape[:2]

    # If already within target width, avoid upscaling to prevent blur
    if og_width <= max_width:
        return image

    scale_factor = max_width / og_width

    new_height = int(og_height * scale_factor)
    new_width = int(max_width)

    # Actual resizing
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    return resized_image
