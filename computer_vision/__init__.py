from typing import Dict, Optional

from config import ocr_config
from pipeline.ocr_pipeline import CardOCRPipeline


DEFAULT_CONFIG = ocr_config.__dict__


def scan_student_id_card(image, config: Optional[Dict] = None) -> Dict:
    """
    Scan student ID card and extract student ID.

    Args:
        image: Camera captured image (BGR format).
        config: Optional configuration overrides.

    Returns:
        {
            'success': bool,
            'student_id': str or None,
            'confidence': float,
            'method': str,
            'error': str or None,
            'processing_time_ms': float
        }
    """
    cfg = config or DEFAULT_CONFIG
    pipeline = CardOCRPipeline(cfg)
    return pipeline.scan_card(image)


__all__ = ["CardOCRPipeline", "scan_student_id_card", "DEFAULT_CONFIG"]
