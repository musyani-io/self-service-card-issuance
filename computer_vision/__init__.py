"""
Computer Vision Package for Self-Service Card Issuance Kiosk.

This package handles camera operations, barcode detection, and image processing
for automated student ID card identification.
"""

from .barcode_reader import BarcodeReader
from .image_capture import ImageCapture
from .exceptions import BarcodeNotFoundError, CameraError, ImageQualityError

__all__ = [
    'BarcodeReader',
    'ImageCapture',
    'BarcodeNotFoundError',
    'CameraError',
    'ImageQualityError',
]
