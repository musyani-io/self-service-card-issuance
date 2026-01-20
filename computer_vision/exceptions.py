"""
Custom exceptions for computer vision module.

Defines specific exception types for different failure scenarios
in barcode detection and image processing.
"""


class CVError(Exception):
    """Base exception for all computer vision errors."""
    pass


class BarcodeNotFoundError(CVError):
    """Raised when barcode cannot be detected in the image."""
    pass


class BarcodeDecodeError(CVError):
    """Raised when barcode is detected but cannot be decoded."""
    pass


class CameraError(CVError):
    """Raised when camera initialization or operation fails."""
    pass


class ImageQualityError(CVError):
    """Raised when image quality is insufficient for processing."""
    
    def __init__(self, message, quality_metrics=None):
        """
        Initialize with quality metrics.
        
        Args:
            message: Error message
            quality_metrics: Dictionary of quality check results
        """
        super().__init__(message)
        self.quality_metrics = quality_metrics or {}


class CaptureError(CVError):
    """Raised when image capture fails."""
    pass


class ConfigurationError(CVError):
    """Raised when camera or module configuration is invalid."""
    pass
