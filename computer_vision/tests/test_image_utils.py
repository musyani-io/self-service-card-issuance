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


class TestGaussianBlur:
    """Tests for gaussian_blur() function."""

    def test_basic_blur_grayscale(self):
        """Apply Gaussian blur to grayscale image."""
        # Create grayscale image with noise
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        result = gaussian_blur(image, ksize=(5, 5), sigma=1.0)
        
        # Output should have same shape
        assert result.shape == (100, 100)
        # Blur should reduce noise (different from input)
        assert not np.array_equal(result, image)

    def test_blur_color_image(self):
        """Apply Gaussian blur to color image."""
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        result = gaussian_blur(image, ksize=(5, 5), sigma=1.0)
        
        # Output should preserve shape and channels
        assert result.shape == (100, 100, 3)

    def test_different_kernel_sizes(self):
        """Test blur with different kernel sizes."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        
        # Test ksize=3, 5, 7
        result_3 = gaussian_blur(image, ksize=(3, 3), sigma=1.0)
        result_5 = gaussian_blur(image, ksize=(5, 5), sigma=1.0)
        result_7 = gaussian_blur(image, ksize=(7, 7), sigma=1.0)
        
        # All should have same shape
        assert result_3.shape == result_5.shape == result_7.shape == (100, 100)
        # Larger kernel = stronger blur (different results)
        assert not np.array_equal(result_3, result_5)

    def test_invalid_even_kernel_size(self):
        """Raise error for even kernel size (must be odd)."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        with pytest.raises(ValueError, match="must be odd"):
            gaussian_blur(image, ksize=(4, 4), sigma=1.0)

    def test_none_image_raises_error(self):
        """Raise error for None image."""
        with pytest.raises(ValueError, match="Input image is None or empty"):
            gaussian_blur(None, ksize=(5, 5), sigma=1.0)


class TestApplyThreshold:
    """Tests for apply_threshold() function."""

    def test_binary_threshold(self):
        """Apply binary thresholding."""
        # Create gradient image
        image = np.arange(0, 256, dtype=np.uint8).reshape(16, 16)
        result = apply_threshold(image, method='binary', thresh=128)
        
        # Result should be binary (0 or 255 only)
        assert np.all((result == 0) | (result == 255))
        assert result.shape == (16, 16)

    def test_otsu_threshold(self):
        """Apply Otsu's automatic thresholding."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        result = apply_threshold(image, method='otsu')
        
        # Result should be binary
        assert np.all((result == 0) | (result == 255))
        assert result.shape == (100, 100)

    def test_adaptive_threshold(self):
        """Apply adaptive thresholding."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        result = apply_threshold(image, method='adaptive', block_size=11, C=2)
        
        # Result should be binary
        assert np.all((result == 0) | (result == 255))
        assert result.shape == (100, 100)

    def test_invalid_threshold_method(self):
        """Raise error for invalid method."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        with pytest.raises(ValueError, match="method must be one of"):
            apply_threshold(image, method='invalid_method')

    def test_invalid_block_size_not_odd(self):
        """Raise error for even block_size in adaptive threshold."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        with pytest.raises(ValueError, match="must be odd"):
            apply_threshold(image, method='adaptive', block_size=10, C=2)


class TestMorphology:
    """Tests for morphology() function."""

    def test_closing_operation(self):
        """Apply morphological closing."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        result = morphology(image, operation='close', ksize=(3, 3), iterations=1)
        
        # Output should have same shape
        assert result.shape == (100, 100)

    def test_opening_operation(self):
        """Apply morphological opening."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        result = morphology(image, operation='open', ksize=(3, 3), iterations=1)
        
        # Output should have same shape
        assert result.shape == (100, 100)

    def test_multiple_iterations(self):
        """Apply morphology with multiple iterations."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        
        result_1 = morphology(image, operation='close', ksize=(3, 3), iterations=1)
        result_2 = morphology(image, operation='close', ksize=(3, 3), iterations=2)
        
        # Both should have same shape
        assert result_1.shape == result_2.shape
        # Results may differ due to repeated application
        assert not np.array_equal(result_1, result_2)

    def test_different_kernel_sizes(self):
        """Test morphology with different kernel sizes."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        
        result_3 = morphology(image, operation='close', ksize=(3, 3), iterations=1)
        result_5 = morphology(image, operation='close', ksize=(5, 5), iterations=1)
        
        # Same shape but different results
        assert result_3.shape == result_5.shape
        assert not np.array_equal(result_3, result_5)

    def test_invalid_operation(self):
        """Raise error for invalid morphology operation."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        with pytest.raises(ValueError, match="operation must be one of"):
            morphology(image, operation='invalid', ksize=(3, 3), iterations=1)


class TestEnhanceContrast:
    """Tests for enhance_contrast() function."""

    def test_clahe_enhancement(self):
        """Apply CLAHE contrast enhancement."""
        # Create low-contrast image
        image = np.random.randint(50, 150, (100, 100), dtype=np.uint8)
        result = enhance_contrast(image, clip_limit=2.0, tile_grid_size=(8, 8))
        
        # Output should have same shape
        assert result.shape == (100, 100)
        # Enhancement should change values
        assert not np.array_equal(result, image)

    def test_color_image_enhancement(self):
        """Apply CLAHE to color image (converts to grayscale first)."""
        image = np.random.randint(50, 150, (100, 100, 3), dtype=np.uint8)
        result = enhance_contrast(image, clip_limit=2.0, tile_grid_size=(8, 8))
        
        # Function converts to grayscale internally, so returns 2D array
        assert result.shape == (100, 100)

    def test_different_clip_limits(self):
        """Test enhancement with different clip limits."""
        image = np.random.randint(50, 150, (100, 100), dtype=np.uint8)
        
        result_low = enhance_contrast(image, clip_limit=1.0, tile_grid_size=(8, 8))
        result_high = enhance_contrast(image, clip_limit=4.0, tile_grid_size=(8, 8))
        
        # Same shape but different results
        assert result_low.shape == result_high.shape
        assert not np.array_equal(result_low, result_high)

    def test_different_tile_sizes(self):
        """Test enhancement with different tile grid sizes."""
        image = np.random.randint(50, 150, (100, 100), dtype=np.uint8)
        
        result_small = enhance_contrast(image, clip_limit=2.0, tile_grid_size=(4, 4))
        result_large = enhance_contrast(image, clip_limit=2.0, tile_grid_size=(16, 16))
        
        # Same shape but different results
        assert result_small.shape == result_large.shape
        assert not np.array_equal(result_small, result_large)

    def test_invalid_clip_limit(self):
        """Raise error for invalid clip limit."""
        image = np.random.randint(50, 150, (100, 100), dtype=np.uint8)
        with pytest.raises(ValueError, match="clip_limit must be between"):
            enhance_contrast(image, clip_limit=-1.0, tile_grid_size=(8, 8))
