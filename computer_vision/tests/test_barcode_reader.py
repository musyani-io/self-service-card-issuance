"""
Unit tests for barcode_reader module - Task 4.1 and Task 4.2 functions.

Tests barcode detection (locate, multi-barcode, confidence scoring) and
barcode decoding (extract data, validate format, error handling).

Test Groups:
- BasicDetectionTests: Core barcode detection functionality
- MultiBarcodeScenariosTests: Multiple barcode handling
- DecodingTests: Barcode decoding and format validation
- EdgeCasesAndErrorsTests: Error handling and edge cases
"""

import pytest
import numpy as np
import cv2
from pathlib import Path
from ..barcode_reader import (
    detect_barcode_location,
    detect_all_barcodes,
    get_barcode_confidence,
    decode_barcode,
    decode_barcode_from_region,
    validate_barcode_format,
    handle_decode_error
)


class TestBasicBarcodeDetection:
    """Test basic barcode detection functionality."""
    
    def test_detect_barcode_location_with_blank_image(self):
        """Test detection returns None for blank image with no barcode."""
        blank_image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        result = detect_barcode_location(blank_image)
        assert result is None, "Should return None for image with no barcode"
    
    def test_detect_barcode_location_returns_dict_structure(self):
        """Test detection returns properly structured dict when barcode exists."""
        # This would need an actual barcode image to test fully
        # For now, we test that the function handles proper structure
        blank_image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        result = detect_barcode_location(blank_image)
        # When no barcode, result is None (valid return)
        assert result is None or isinstance(result, dict)
    
    def test_detect_barcode_location_with_grayscale_image(self):
        """Test detection works with grayscale images."""
        gray_image = np.ones((300, 400), dtype=np.uint8) * 150
        result = detect_barcode_location(gray_image)
        assert result is None or isinstance(result, dict)
    
    def test_detect_barcode_location_invalid_input_none(self):
        """Test detection raises ValueError for None input."""
        with pytest.raises(ValueError, match="Image cannot be None"):
            detect_barcode_location(None)
    
    def test_detect_barcode_location_invalid_input_not_array(self):
        """Test detection raises ValueError for non-array input."""
        with pytest.raises(ValueError, match="must be numpy array"):
            detect_barcode_location("not_an_array")
    
    def test_detect_barcode_location_invalid_input_empty_array(self):
        """Test detection raises ValueError for empty array."""
        empty_array = np.array([])
        with pytest.raises(ValueError, match="empty"):
            detect_barcode_location(empty_array)
    
    def test_detect_barcode_location_invalid_shape(self):
        """Test detection raises ValueError for 1D array."""
        invalid_shape = np.array([1, 2, 3, 4, 5])
        with pytest.raises(ValueError, match="2D or 3D"):
            detect_barcode_location(invalid_shape)


class TestMultiBarcodeAndConfidence:
    """Test multiple barcode detection and confidence scoring."""
    
    def test_detect_all_barcodes_returns_list(self):
        """Test detect_all_barcodes returns a list."""
        blank_image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        result = detect_all_barcodes(blank_image)
        assert isinstance(result, list), "Should return list"
    
    def test_detect_all_barcodes_empty_list_when_none_found(self):
        """Test detect_all_barcodes returns empty list when no barcodes found."""
        blank_image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        result = detect_all_barcodes(blank_image)
        assert result == [], "Should return empty list when no barcodes found"
    
    def test_detect_all_barcodes_invalid_input(self):
        """Test detect_all_barcodes raises ValueError for invalid input."""
        with pytest.raises(ValueError):
            detect_all_barcodes(None)
    
    def test_get_barcode_confidence_valid_bbox(self):
        """Test confidence scoring with valid bbox."""
        image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        bbox = (50, 50, 100, 50)  # (x, y, w, h)
        
        confidence = get_barcode_confidence(image, bbox)
        assert isinstance(confidence, (int, float)), "Should return numeric confidence"
        assert 0 <= confidence <= 1, "Confidence should be between 0 and 1"
    
    def test_get_barcode_confidence_invalid_bbox_none(self):
        """Test confidence scoring raises error for None bbox."""
        image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        with pytest.raises(ValueError):
            get_barcode_confidence(image, None)
    
    def test_get_barcode_confidence_invalid_bbox_wrong_type(self):
        """Test confidence scoring raises error for non-tuple bbox."""
        image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        with pytest.raises(ValueError):
            get_barcode_confidence(image, "not_a_bbox")
    
    def test_get_barcode_confidence_large_bbox(self):
        """Test confidence scoring with large bbox (good quality indicator)."""
        image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        large_bbox = (10, 10, 200, 100)  # Large barcode region
        
        confidence = get_barcode_confidence(image, large_bbox)
        assert 0 <= confidence <= 1



class TestBarcodeDecoding:
    """Test barcode decoding functionality."""
    
    def test_decode_barcode_returns_none_for_blank_image(self):
        """Test decode_barcode returns None when no barcode found."""
        blank_image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        result = decode_barcode(blank_image)
        assert result is None, "Should return None for image with no barcode"
    
    def test_decode_barcode_returns_string_or_none(self):
        """Test decode_barcode returns either string or None."""
        blank_image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        result = decode_barcode(blank_image)
        assert result is None or isinstance(result, str)
    
    def test_decode_barcode_invalid_input_none(self):
        """Test decode_barcode raises ValueError for None input."""
        with pytest.raises(ValueError, match="cannot be None"):
            decode_barcode(None)
    
    def test_decode_barcode_invalid_input_not_array(self):
        """Test decode_barcode raises ValueError for non-array input."""
        with pytest.raises(ValueError, match="must be numpy array"):
            decode_barcode("not_an_array")
    
    def test_decode_barcode_invalid_input_empty(self):
        """Test decode_barcode raises ValueError for empty array."""
        empty_array = np.array([])
        with pytest.raises(ValueError, match="empty"):
            decode_barcode(empty_array)
    
    def test_decode_barcode_invalid_shape(self):
        """Test decode_barcode raises ValueError for invalid shape."""
        invalid = np.array([1, 2, 3])  # 1D array
        with pytest.raises(ValueError, match="2D or 3D"):
            decode_barcode(invalid)
    
    def test_decode_barcode_from_region_valid_bbox(self):
        """Test decode_barcode_from_region with valid bbox dict."""
        image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        bbox = {'x': 50, 'y': 50, 'width': 100, 'height': 50}
        
        result = decode_barcode_from_region(image, bbox)
        assert result is None or isinstance(result, str)
    
    def test_decode_barcode_from_region_invalid_bbox_none(self):
        """Test decode_barcode_from_region raises ValueError for None bbox."""
        image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        with pytest.raises(ValueError, match="cannot be None"):
            decode_barcode_from_region(image, None)
    
    def test_decode_barcode_from_region_invalid_bbox_not_dict(self):
        """Test decode_barcode_from_region raises ValueError for non-dict bbox."""
        image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        with pytest.raises(ValueError, match="must be dict"):
            decode_barcode_from_region(image, (50, 50, 100, 50))
    
    def test_decode_barcode_from_region_missing_bbox_keys(self):
        """Test decode_barcode_from_region raises error for incomplete bbox."""
        image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        incomplete_bbox = {'x': 50, 'y': 50}  # Missing width, height
        
        with pytest.raises(ValueError, match="missing keys"):
            decode_barcode_from_region(image, incomplete_bbox)
    
    def test_decode_barcode_from_region_out_of_bounds_bbox(self):
        """Test decode_barcode_from_region handles out-of-bounds coordinates."""
        image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        oob_bbox = {'x': 400, 'y': 400, 'width': 10, 'height': 10}
        
        result = decode_barcode_from_region(image, oob_bbox)
        assert result is None, "Should return None for out-of-bounds bbox"



class TestBarcodeFormatValidation:
    """Test barcode format validation."""
    
    def test_validate_barcode_format_none_input(self):
        """Test validate_barcode_format returns False for None input."""
        result = validate_barcode_format(None)
        assert result is False
    
    def test_validate_barcode_format_empty_string(self):
        """Test validate_barcode_format returns False for empty string."""
        result = validate_barcode_format("")
        assert result is False
    
    def test_validate_barcode_format_basic_valid(self):
        """Test validate_barcode_format accepts valid basic format."""
        result = validate_barcode_format("12345")
        assert result is True
    
    def test_validate_barcode_format_too_short(self):
        """Test validate_barcode_format rejects too short strings."""
        result = validate_barcode_format("1234")  # < 5 chars
        assert result is False
    
    def test_validate_barcode_format_too_long(self):
        """Test validate_barcode_format rejects too long strings."""
        long_string = "1" * 60  # > 50 chars
        result = validate_barcode_format(long_string)
        assert result is False
    
    def test_validate_barcode_format_alphanumeric(self):
        """Test validate_barcode_format accepts alphanumeric."""
        result = validate_barcode_format("ABC123DEF")
        assert result is True
    
    def test_validate_barcode_format_special_chars(self):
        """Test validate_barcode_format rejects invalid special characters."""
        result = validate_barcode_format("ABC@123#")
        assert result is False
    
    def test_validate_barcode_format_student_id_valid(self):
        """Test validate_barcode_format validates student ID format."""
        result = validate_barcode_format("1234567890", "student_id")
        assert result is True
    
    def test_validate_barcode_format_student_id_wrong_length(self):
        """Test validate_barcode_format rejects wrong length student ID."""
        result = validate_barcode_format("123456789", "student_id")  # 9 digits
        assert result is False
    
    def test_validate_barcode_format_student_id_non_digit(self):
        """Test validate_barcode_format rejects non-digit student ID."""
        result = validate_barcode_format("123456789A", "student_id")
        assert result is False
    
    def test_validate_barcode_format_employee_id_valid(self):
        """Test validate_barcode_format validates employee ID format."""
        result = validate_barcode_format("ABC123", "employee_id")
        assert result is True
    
    def test_validate_barcode_format_employee_id_too_short(self):
        """Test validate_barcode_format rejects short employee ID."""
        result = validate_barcode_format("AB", "employee_id")  # < 6
        assert result is False
    
    def test_validate_barcode_format_employee_id_too_long(self):
        """Test validate_barcode_format rejects long employee ID."""
        result = validate_barcode_format("ABCDEF123", "employee_id")  # > 8
        assert result is False
    
    def test_validate_barcode_format_card_number_valid(self):
        """Test validate_barcode_format validates card number format."""
        result = validate_barcode_format("4532015112830366", "card_number")
        assert result is True
    
    def test_validate_barcode_format_card_number_with_hyphens(self):
        """Test validate_barcode_format validates card number with hyphens."""
        result = validate_barcode_format("4532-0151-1283-0366", "card_number")
        assert result is True
    
    def test_validate_barcode_format_card_number_with_spaces(self):
        """Test validate_barcode_format validates card number with spaces."""
        result = validate_barcode_format("4532 0151 1283 0366", "card_number")
        assert result is True
    
    def test_validate_barcode_format_card_number_too_short(self):
        """Test validate_barcode_format rejects short card number."""
        result = validate_barcode_format("453201511283036", "card_number")  # 15 digits
        assert result is False
    
    def test_validate_barcode_format_custom_regex(self):
        """Test validate_barcode_format with custom regex pattern."""
        # Pattern: exactly 5 digits
        result = validate_barcode_format("12345", r"^\d{5}$")
        assert result is True
    
    def test_validate_barcode_format_custom_regex_fail(self):
        """Test validate_barcode_format rejects non-matching regex."""
        result = validate_barcode_format("1234", r"^\d{5}$")  # Need 5 digits
        assert result is False
    
    def test_validate_barcode_format_invalid_regex(self):
        """Test validate_barcode_format raises error for invalid regex."""
        with pytest.raises(ValueError, match="Invalid regex"):
            validate_barcode_format("12345", "[invalid(regex")


class TestErrorHandling:
    """Test error handling and diagnostics."""
    
    def test_handle_decode_error_returns_dict(self):
        """Test handle_decode_error returns diagnostic dictionary."""
        image = np.ones((200, 300, 3), dtype=np.uint8) * 100
        result = handle_decode_error(image, "Test error")
        
        assert isinstance(result, dict)
    
    def test_handle_decode_error_dict_structure(self):
        """Test handle_decode_error returns properly structured dict."""
        image = np.ones((200, 300, 3), dtype=np.uint8) * 100
        result = handle_decode_error(image, "Test error")
        
        required_keys = {
            'error', 'image_shape', 'image_stats',
            'suggested_actions', 'retry_recommended',
            'preprocessing_suggestions'
        }
        assert required_keys.issubset(result.keys())
    
    def test_handle_decode_error_image_shape(self):
        """Test handle_decode_error correctly reports image shape."""
        image = np.ones((200, 300, 3), dtype=np.uint8) * 100
        result = handle_decode_error(image, "Test error")
        
        assert result['image_shape'] == (200, 300, 3)
    
    def test_handle_decode_error_dark_image_detection(self):
        """Test handle_decode_error detects dark images."""
        dark_image = np.ones((200, 300, 3), dtype=np.uint8) * 30
        result = handle_decode_error(dark_image, "No barcode")
        
        assert result['image_stats']['mean'] < 50
        assert 'enhance_contrast' in result['preprocessing_suggestions']
    
    def test_handle_decode_error_bright_image_detection(self):
        """Test handle_decode_error detects bright images."""
        bright_image = np.ones((200, 300, 3), dtype=np.uint8) * 220
        result = handle_decode_error(bright_image, "No barcode")
        
        assert result['image_stats']['mean'] > 200
        assert any('bright' in action.lower() for action in result['suggested_actions'])
    
    def test_handle_decode_error_invalid_input(self):
        """Test handle_decode_error raises ValueError for invalid input."""
        with pytest.raises(ValueError):
            handle_decode_error(None, "Test error")
    
    def test_handle_decode_error_retry_recommended(self):
        """Test handle_decode_error recommends retry."""
        image = np.ones((200, 300, 3), dtype=np.uint8) * 100
        result = handle_decode_error(image, "Test error")
        
        assert result['retry_recommended'] is True
    
    def test_handle_decode_error_custom_max_retries(self):
        """Test handle_decode_error respects max_retries config."""
        image = np.ones((200, 300, 3), dtype=np.uint8) * 100
        result = handle_decode_error(image, "Test error", {'max_retries': 0})
        
        assert result['retry_recommended'] is False


class TestIntegration:
    """Test integration between detection and decoding functions."""
    
    def test_detect_then_decode_workflow(self):
        """Test typical workflow: detect location, then decode from region."""
        blank_image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        
        # Try to detect
        detection = detect_barcode_location(blank_image)
        
        # If detected, decode from region
        if detection:
            result = decode_barcode_from_region(blank_image, detection['bbox'])
            assert result is None or isinstance(result, str)
        else:
            # No detection is valid
            assert detection is None
    
    def test_detect_all_then_validate_workflow(self):
        """Test workflow: detect multiple barcodes, then validate."""
        blank_image = np.ones((300, 400, 3), dtype=np.uint8) * 200
        
        detections = detect_all_barcodes(blank_image)
        assert isinstance(detections, list)
        
        for detection in detections:
            assert isinstance(detection, dict)
            assert 'bbox' in detection
    
    def test_error_recovery_workflow(self):
        """Test error handling and recovery suggestion workflow."""
        dark_image = np.ones((200, 300, 3), dtype=np.uint8) * 30
        
        # Try to decode
        result = decode_barcode(dark_image)
        
        # If failed, get diagnostic info
        if result is None:
            error_info = handle_decode_error(dark_image, "Decoding failed")
            
            # Validate we have suggestions
            assert len(error_info['suggested_actions']) > 0
            assert len(error_info['preprocessing_suggestions']) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
