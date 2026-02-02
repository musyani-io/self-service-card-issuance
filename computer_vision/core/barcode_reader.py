from typing import List, Dict
import numpy as np
from pyzbar.pyzbar import decode

def detect_barcode(image: np.ndarray) -> List[Dict]:
    """
    Detect barcode regions and return bounding boxes
    """

    # Checks for validity of image
    if image is None:
        raise ValueError("Image cannot be None")

    # Checks for image's type
    if not isinstance(image, np.ndarray):
        raise ValueError(f"Image must be NumPy array. Received: {type(image)}")
    
    # Checks for empty image
    if image.size == 0:
        raise ValueError("Image is empty.")
    
    results = decode(image)

    detections: List[Dict] = []
    for regions in results:
        x, y, w, h = regions.rect
        detections.append({"bbox": (x, y, w, h), "type": regions.type})

    return detections