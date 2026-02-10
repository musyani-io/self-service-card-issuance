import re
from typing import Optional, Tuple


OCR_CORRECTIONS = {
    "O": "0",
    "I": "1",
    "L": "1",
    "S": "5",
    "B": "8",
}


def normalize_ocr_text(text: str) -> str:
    """
    Normalize OCR text by fixing common character confusions.
    """
    if not text:
        return ""

    normalized = []
    for ch in text:
        normalized.append(OCR_CORRECTIONS.get(ch, ch))
    return "".join(normalized)


def extract_student_id(text: str, pattern: str) -> str:
    """
    Extract the first student ID match from text using the provided regex pattern.
    """
    match = re.search(pattern, text)
    return match.group(0) if match else ""


def validate_student_id(
    student_id: str,
    pattern: str,
    valid_year_range: Tuple[int, int],
    total_length: int,
) -> bool:
    """
    Validate student ID by pattern, length, and year range.
    """
    if not student_id:
        return False

    if len(student_id) != total_length:
        return False

    if re.fullmatch(pattern, student_id) is None:
        return False

    year_str = student_id.split("-")[0]
    if not year_str.isdigit():
        return False

    year = int(year_str)
    return valid_year_range[0] <= year <= valid_year_range[1]


def extract_and_validate_student_id(
    text: str,
    pattern: str,
    valid_year_range: Tuple[int, int],
    total_length: int,
) -> Optional[str]:
    """
    Extract and validate student ID. Returns the ID or None if invalid.
    """
    candidate = extract_student_id(text, pattern)
    if validate_student_id(candidate, pattern, valid_year_range, total_length):
        return candidate

    corrected_text = normalize_ocr_text(text)
    candidate = extract_student_id(corrected_text, pattern)
    if validate_student_id(candidate, pattern, valid_year_range, total_length):
        return candidate

    return None
