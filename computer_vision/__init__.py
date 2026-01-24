"""
Computer Vision Package for Self-Service Card Issuance Kiosk.

This package handles camera operations, barcode detection, and image processing
for automated student ID card identification.
"""

from .image_capture import ImageCapture
from .exceptions import BarcodeNotFoundError, CameraError, ImageQualityError

__all__ = [
    'ImageCapture',
    'BarcodeNotFoundError',
    'CameraError',
    'ImageQualityError',
]
