# OCR API Reference

## Module: computer_vision

### scan_student_id_card(image, config=None)

Scans a card image and returns a structured OCR result.

### Parameters

- `image`: BGR image (NumPy array)
- `config` (optional): config dict override

### Scans

```bash
{
  'success': bool,
  'student_id': str | None,
  'confidence': float,
  'method': str,
  'error': str | None,
  'processing_time_ms': float
}
```

## Pipeline: CardOCRPipeline

Located at [computer_vision/pipeline/ocr_pipeline.py](computer_vision/pipeline/ocr_pipeline.py).

### scan_card(image)

Runs detection → correction → ROI → OCR → validation.

## Notes

- Configure OCR settings in [computer_vision/config/ocr_config.py](computer_vision/config/ocr_config.py).
- Use [examples/basic_usage.py](examples/basic_usage.py) for a minimal example.
