"""
Unit tests for image_utils preprocessing functions.

Tests cover basic functions, advanced preprocessing, pipeline,
and utility functions for barcode detection preprocessing.
"""

import pytest
import numpy as np
import cv2
import os
import tempfile
from pathlib import Path

# Import functions to test
from computer_vision.image_utils import (
    convert_to_grayscale,
    resize_image,
    crop_roi,
    gaussian_blur,
    apply_threshold,
    morphology,
    enhance_contrast,
    preprocess_image,
    save_debug_image,
)

class TestConvertToGrayscale:
    """Tests for convert_to_grayscale() function."""

    def test_bgr_to_grayscale(self):
        """Convert BGR color image to grayscale."""
        # Create BGR image (3 channels)
        bgr_image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        result = convert_to_grayscale(bgr_image)
        
        # Verify output is grayscale (2D array)
        assert len(result.shape) == 2
        assert result.shape == (100, 100)

    def test_already_grayscale(self):
        """Return grayscale image unchanged."""
        # Create grayscale image (2D array)
        gray_image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        result = convert_to_grayscale(gray_image)
        
        # Should be identical (same object or equal values)
        assert np.array_equal(result, gray_image)

    def test_rgba_to_grayscale(self):
        """Convert RGBA (4-channel) image to grayscale."""
        # Create RGBA image (4 channels)
        rgba_image = np.random.randint(0, 256, (100, 100, 4), dtype=np.uint8)
        result = convert_to_grayscale(rgba_image)
        
        # Verify output is grayscale
        assert len(result.shape) == 2
        assert result.shape == (100, 100)

    def test_none_image_raises_error(self):
        """Raise ValueError for None image."""
        with pytest.raises(ValueError, match="Input image is None or empty"):
            convert_to_grayscale(None)

    def test_empty_image_raises_error(self):
        """Raise ValueError for empty image."""
        empty_image = np.array([], dtype=np.uint8)
        with pytest.raises(ValueError, match="Input image is None or empty"):
            convert_to_grayscale(empty_image)


class TestResizeImage:
    """Tests for resize_image() function."""

    def test_resize_with_aspect_ratio(self):
        """Resize image maintaining aspect ratio."""
        # Create image 1000x600 (aspect ratio 5:3)
        image = np.random.randint(0, 256, (600, 1000, 3), dtype=np.uint8)
        result = resize_image(image, target_width=500)
        
        # New width should be 500, height should scale accordingly
        assert result.shape[1] == 500
        # Height should be 300 (maintaining 5:3 ratio)
        assert result.shape[0] == 300

    def test_resize_without_aspect_ratio(self):
        """Resize image without maintaining aspect ratio (stretch)."""
        image = np.random.randint(0, 256, (600, 1000, 3), dtype=np.uint8)
        result = resize_image(image, target_width=500, maintain_aspect=False)
        
        # Width changes, height stays same
        assert result.shape[1] == 500
        assert result.shape[0] == 600

    def test_minimum_width_enforcement(self):
        """Enforce minimum width limit."""
        image = np.random.randint(0, 256, (600, 200, 3), dtype=np.uint8)
        # Request width below minimum (default 150), but within shrinkage ratio
        result = resize_image(image, target_width=100, min_width=150, max_shrink_ratio=0.6)
        
        # Should resize to min_width (150) since it's higher than requested (100)
        assert result.shape[1] == 150

    def test_shrinkage_ratio_enforcement(self):
        """Enforce maximum shrinkage ratio."""
        image = np.random.randint(0, 256, (600, 1000, 3), dtype=np.uint8)
        # max_shrink_ratio=0.5 means don't shrink below 50%
        # Original width 1000, min allowed 500
        # Requesting 300 should raise error
        with pytest.raises(ValueError, match="exceeds max shrinkage"):
            resize_image(image, target_width=300, max_shrink_ratio=0.5)

    def test_invalid_target_width(self):
        """Raise error for invalid target width."""
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        with pytest.raises(ValueError, match="target_width must be positive"):
            resize_image(image, target_width=-50)


class TestCropROI:
    """Tests for crop_roi() function."""

    def test_default_bottom_half_crop(self):
        """Crop bottom half by default."""
        # Create 100x200 image (height=200)
        image = np.random.randint(0, 256, (200, 100, 3), dtype=np.uint8)
        result = crop_roi(image)
        
        # Should crop bottom half: height should be ~100
        assert result.shape[0] == 100
        assert result.shape[1] == 100

    def test_custom_coordinates_crop(self):
        """Crop specific region with custom coordinates."""
        image = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        result = crop_roi(image, x=50, y=50, width=100, height=100)
        
        # Should crop 100x100 region starting at (50, 50), preserving channels
        assert result.shape == (100, 100, 3)

    def test_crop_boundary_clipping(self):
        """Clip ROI to image boundaries."""
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        # Request region extending beyond boundaries
        result = crop_roi(image, x=50, y=50, width=200, height=200)
        
        # Should clip to available area: 50x50, preserving channels
        assert result.shape == (50, 50, 3)

    def test_invalid_negative_coordinates(self):
        """Raise error for negative coordinates."""
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        with pytest.raises(ValueError, match="non-negative"):
            crop_roi(image, x=-10, y=10, width=50, height=50)

    def test_out_of_bounds_roi_raises_error(self):
        """Raise error when ROI start is outside image."""
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        with pytest.raises(ValueError, match="outside image bounds"):
            crop_roi(image, x=200, y=50, width=50, height=50)
