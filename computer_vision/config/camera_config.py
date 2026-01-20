"""
Camera configuration parameters.

Defines camera settings for optimal barcode detection in kiosk environment.
"""


class CameraConfig:
    """
    Camera configuration parameters for Raspberry Pi camera.
    """
    
    def __init__(
        self,
        resolution=(1920, 1080),
        framerate=30,
        exposure_mode='auto',
        exposure_compensation=0,
        iso=0,
        brightness=50,
        contrast=0,
        sharpness=0,
        focus_mode='auto',
        awb_mode='auto',
        roi=None
    ):
        """
        Initialize camera configuration.
        
        Args:
            resolution: Capture resolution (width, height)
            framerate: Frames per second
            exposure_mode: Exposure control mode ('auto', 'manual', 'sports', etc.)
            exposure_compensation: Exposure compensation value (-25 to 25)
            iso: ISO sensitivity (0 for auto, or 100-800)
            brightness: Brightness level (0-100)
            contrast: Contrast level (-100 to 100)
            sharpness: Sharpness level (-100 to 100)
            focus_mode: Focus mode ('auto', 'manual', 'continuous')
            awb_mode: Auto white balance mode ('auto', 'sunlight', 'fluorescent', etc.)
            roi: Region of interest (x, y, w, h) for focused capture
        """
        self.resolution = resolution
        self.framerate = framerate
        self.exposure_mode = exposure_mode
        self.exposure_compensation = exposure_compensation
        self.iso = iso
        self.brightness = brightness
        self.contrast = contrast
        self.sharpness = sharpness
        self.focus_mode = focus_mode
        self.awb_mode = awb_mode
        self.roi = roi
    
    def to_dict(self):
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary of configuration parameters
        """
        return {
            'resolution': self.resolution,
            'framerate': self.framerate,
            'exposure_mode': self.exposure_mode,
            'exposure_compensation': self.exposure_compensation,
            'iso': self.iso,
            'brightness': self.brightness,
            'contrast': self.contrast,
            'sharpness': self.sharpness,
            'focus_mode': self.focus_mode,
            'awb_mode': self.awb_mode,
            'roi': self.roi
        }
    
    @classmethod
    def from_dict(cls, config_dict):
        """
        Create configuration from dictionary.
        
        Args:
            config_dict: Dictionary of configuration parameters
            
        Returns:
            CameraConfig instance
        """
        return cls(**config_dict)


def get_default_config():
    """
    Get default camera configuration optimized for barcode detection.
    
    Returns:
        CameraConfig instance with default settings
    """
    return CameraConfig(
        resolution=(1920, 1080),  # Full HD for clear barcode capture
        framerate=30,
        exposure_mode='auto',
        iso=0,  # Auto ISO
        brightness=50,
        sharpness=50,  # Enhanced sharpness for barcode edges
        focus_mode='auto'
    )
