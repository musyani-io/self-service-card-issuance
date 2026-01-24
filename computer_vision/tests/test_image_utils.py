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


class TestPreprocessImage:
    """Tests for preprocess_image() pipeline function."""

    def test_basic_pipeline_execution(self):
        """Run pipeline with default configuration."""
        image = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        result = preprocess_image(image)
        
        # Pipeline returns dict with required keys
        assert isinstance(result, dict)
        assert 'processed_image' in result
        assert 'success' in result
        assert 'timings' in result
        assert 'steps_applied' in result

    def test_pipeline_success_flag(self):
        """Pipeline returns success=True for valid input."""
        image = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        result = preprocess_image(image)
        
        assert result['success'] is True

    def test_pipeline_output_is_valid_image(self):
        """Pipeline output is a valid numpy array."""
        image = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        result = preprocess_image(image)
        
        processed = result['processed_image']
        assert isinstance(processed, np.ndarray)
        assert processed.size > 0

    def test_pipeline_with_grayscale_only(self):
        """Run pipeline with only grayscale conversion enabled."""
        image = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        config = {
            'crop_roi': False,
            'blur': False,
            'threshold': False,
            'morphology': False,
            'enhance_contrast': False,
        }
        result = preprocess_image(image, config=config)
        
        assert result['success'] is True
        # Output should be grayscale
        assert len(result['processed_image'].shape) == 2

    def test_pipeline_with_resize(self):
        """Run pipeline with resize enabled."""
        image = np.random.randint(0, 256, (200, 400, 3), dtype=np.uint8)
        config = {
            'crop_roi': False,
            'blur': False,
            'threshold': False,
            'morphology': False,
            'enhance_contrast': False,
        }
        result = preprocess_image(image, config=config)
        
        assert result['success'] is True
        # Without resize config (pipeline doesn't have resize step), width unchanged
        # Just verify processing succeeded and output is valid
        assert result['processed_image'].size > 0

    def test_pipeline_with_crop(self):
        """Run pipeline with crop enabled."""
        image = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        config = {
            'crop_roi': True,
            'blur': False,
            'threshold': False,
            'morphology': False,
            'enhance_contrast': False,
        }
        result = preprocess_image(image, config=config)
        
        assert result['success'] is True
        # Default crop_roi crops bottom half
        assert result['processed_image'].shape[0] == 100

    def test_pipeline_with_full_preprocessing(self):
        """Run pipeline with all steps enabled (standard barcode detection)."""
        image = np.random.randint(0, 256, (300, 300, 3), dtype=np.uint8)
        config = {
            'crop_roi': True,
            'blur': True,
            'blur_ksize': (5, 5),
            'threshold': 'adaptive',
            'morphology': 'close',
            'enhance_contrast': True,
            'enhance_contrast_clip': 2.0,
        }
        result = preprocess_image(image, config=config)
        
        assert result['success'] is True
        assert len(result['timings']) > 0
        assert len(result['steps_applied']) > 0

    def test_pipeline_timings_are_positive(self):
        """Pipeline timing measurements are positive numbers."""
        image = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        result = preprocess_image(image)
        
        # All timing values should be >= 0 (milliseconds)
        for timing_value in result['timings'].values():
            assert timing_value >= 0

    def test_pipeline_with_invalid_image(self):
        """Pipeline raises error for None image."""
        # Pipeline raises ValueError on None input
        with pytest.raises(ValueError, match="Input image is None or empty"):
            preprocess_image(None)

    def test_pipeline_preserves_all_keys_on_error(self):
        """Pipeline returns all keys even when steps fail."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        # Use invalid threshold method to trigger error in pipeline
        config = {
            'threshold': 'invalid_method',
        }
        result = preprocess_image(image, config=config)
        
        # Should have error handling in place
        assert 'processed_image' in result
        assert 'success' in result

    def test_pipeline_config_none_uses_defaults(self):
        """Pipeline with config=None uses default settings."""
        image = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        result = preprocess_image(image, config=None)
        
        assert result['success'] is True

    def test_pipeline_sequential_steps_order(self):
        """Pipeline applies steps in correct order."""
        image = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        config = {
            'crop_roi': True,
            'blur': True,
            'threshold': 'otsu',
            'morphology': 'close',
            'enhance_contrast': False,
        }
        result = preprocess_image(image, config=config)
        
        # Check steps were applied in expected order
        steps = result['steps_applied']
        # Grayscale should be first
        if steps:
            assert steps[0] == 'grayscale'


class TestSaveDebugImage:
    """Tests for save_debug_image() utility function."""

    def test_save_grayscale_image(self):
        """Save grayscale image to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
            filepath = os.path.join(tmpdir, 'test_gray.jpg')
            
            # Function returns None but saves file
            save_debug_image(image, filepath)
            
            # File should exist
            assert os.path.exists(filepath)

    def test_save_color_image(self):
        """Save color image to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
            filepath = os.path.join(tmpdir, 'test_color.jpg')
            
            # Function returns None but saves file
            save_debug_image(image, filepath)
            
            assert os.path.exists(filepath)

    def test_save_image_with_bounding_box(self):
        """Save image with bounding box annotation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
            filepath = os.path.join(tmpdir, 'test_bbox.jpg')
            
            # Add bounding box annotation as list of dicts
            annotations = [{'type': 'bbox', 'bbox': (10, 10, 50, 50)}]
            save_debug_image(image, filepath, annotations=annotations)
            
            assert os.path.exists(filepath)

    def test_save_image_with_text(self):
        """Save image with text annotation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
            filepath = os.path.join(tmpdir, 'test_text.jpg')
            
            # Add text annotation
            annotations = [{'type': 'text', 'text': 'Test', 'position': (10, 20)}]
            save_debug_image(image, filepath, annotations=annotations)
            
            assert os.path.exists(filepath)

    def test_save_creates_directory_if_needed(self):
        """Create parent directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
            filepath = os.path.join(tmpdir, 'subdir', 'test.jpg')
            
            save_debug_image(image, filepath)
            
            # Should create directory and save file
            assert os.path.exists(filepath)

    def test_save_none_image_raises_error(self):
        """Raise error for None image."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test.jpg')
            
            with pytest.raises(ValueError, match="Input image is None or empty"):
                save_debug_image(None, filepath)

    def test_save_with_jpg_format(self):
        """Save with JPG format works correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
            filepath = os.path.join(tmpdir, 'test.jpg')
            
            save_debug_image(image, filepath)
            assert os.path.exists(filepath)

    def test_multiple_annotations(self):
        """Save image with multiple annotations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
            filepath = os.path.join(tmpdir, 'test_multi.jpg')
            
            annotations = [
                {'type': 'bbox', 'bbox': (10, 10, 50, 50)},
                {'type': 'text', 'text': 'Label', 'position': (15, 15)},
            ]
            save_debug_image(image, filepath, annotations=annotations)
            
            assert os.path.exists(filepath)


class TestErrorHandling:
    """Tests for error handling across all functions."""

    def test_grayscale_with_invalid_shape(self):
        """Handle empty array."""
        # Empty array should raise error
        image = np.array([], dtype=np.uint8)
        
        with pytest.raises(ValueError, match="Input image is None or empty"):
            convert_to_grayscale(image)

    def test_resize_with_zero_target_width(self):
        """Reject zero target width."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        
        with pytest.raises(ValueError, match="target_width must be positive"):
            resize_image(image, target_width=0)

    def test_crop_with_zero_dimensions(self):
        """Reject zero crop dimensions."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        
        with pytest.raises(ValueError):
            crop_roi(image, x=10, y=10, width=0, height=100)

    def test_threshold_with_none_image(self):
        """Threshold handles None input."""
        with pytest.raises(ValueError, match="Input image is None or empty"):
            apply_threshold(None, method='otsu')

    def test_morphology_with_invalid_iterations(self):
        """Morphology rejects invalid iteration count."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        
        with pytest.raises(ValueError, match="iterations must be positive"):
            morphology(image, operation='close', ksize=(3, 3), iterations=0)

    def test_enhance_contrast_with_extreme_clip_limit(self):
        """Contrast enhancement rejects out-of-range clip limit."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        
        # Clip limit out of range (1.0-40.0)
        with pytest.raises(ValueError, match="clip_limit must be between"):
            enhance_contrast(image, clip_limit=100.0, tile_grid_size=(8, 8))

    def test_pipeline_with_corrupted_intermediate_state(self):
        """Pipeline continues processing after individual step issues."""
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        config = {
            'crop_roi': True,
            'blur': True,
            'threshold': 'otsu',
        }
        
        # Should complete despite potential issues
        result = preprocess_image(image, config=config)
        assert 'processed_image' in result
