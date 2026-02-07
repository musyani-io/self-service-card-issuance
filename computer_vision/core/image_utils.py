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
        raise ValueError(
            f"Image must be a NumPy array. Received type: {str(type(image))}"
        )

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
        np.ndarray: Resized image with new shape (new_height, new_width)

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

    scale_factor = max_width / og_width

    new_height = int(og_height * scale_factor)
    new_width = int(max_width)

    # Actual resizing (supports both upscaling and downscaling)
    resized_image = cv2.resize(
        image, (new_width, new_height), interpolation=cv2.INTER_LINEAR
    )

    return resized_image


def crop_roi(image: np.ndarray) -> np.ndarray:
    """
    Crops Region of Interest (ROI)

    Parameters:
        image(np.ndarray): Input image

    Returns:
        np.ndarray: A cropped image (bottom half as interest where the barcode lives)

    Raises:
        ValueError: If the image is not NumPy, is None
    """

    # Checks for validity of image
    if image is None:
        raise ValueError("Image cannot be None")

    # Checks for image's type
    if not isinstance(image, np.ndarray):
        raise ValueError(f"Image must be NumPy array. Received: {type(image)}")

    # Obtain dimensions
    image_height, image_width = image.shape[:2]

    # Cropping the bottom half
    image_roi = image[image_height // 2 : image_height, 0:image_width]

    return image_roi


def enhance_contrast(image: np.ndarray) -> np.ndarray:
    """
    Enhance contrast using CLAHE for better OCR readability.

    Parameters:
        image(np.ndarray): Grayscale image

    Returns:
        np.ndarray: Contrast-enhanced image
    """
    if image is None:
        raise ValueError("Image cannot be None")
    if not isinstance(image, np.ndarray):
        raise ValueError(f"Image must be NumPy array. Received: {type(image)}")

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(image)


def denoise_image(image: np.ndarray) -> np.ndarray:
    """
    Denoise image using Non-Local Means.

    Parameters:
        image(np.ndarray): Grayscale image

    Returns:
        np.ndarray: Denoised image
    """
    if image is None:
        raise ValueError("Image cannot be None")
    if not isinstance(image, np.ndarray):
        raise ValueError(f"Image must be NumPy array. Received: {type(image)}")

    return cv2.fastNlMeansDenoising(image, None, 10, 7, 21)


def binarize_image(image: np.ndarray) -> np.ndarray:
    """
    Binarize image using adaptive thresholding for OCR.

    Parameters:
        image(np.ndarray): Grayscale image

    Returns:
        np.ndarray: Binarized image
    """
    if image is None:
        raise ValueError("Image cannot be None")
    if not isinstance(image, np.ndarray):
        raise ValueError(f"Image must be NumPy array. Received: {type(image)}")

    return cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10
    )


def preprocess_for_ocr(image: np.ndarray) -> np.ndarray:
    """
    Preprocess ROI image for OCR by chaining:
    grayscale -> denoise -> contrast -> binarize

    Parameters:
        image(np.ndarray): BGR or grayscale image

    Returns:
        np.ndarray: Preprocessed binary image suitable for OCR
    """
    if image is None:
        raise ValueError("Image cannot be None")
    if not isinstance(image, np.ndarray):
        raise ValueError(f"Image must be NumPy array. Received: {type(image)}")

    # Convert to grayscale if needed
    if len(image.shape) == 3 and image.shape[2] == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    gray = denoise_image(gray)
    gray = enhance_contrast(gray)
    binary = binarize_image(gray)

    return binary
