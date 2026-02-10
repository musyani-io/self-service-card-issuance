"""
Run OCR on a card image and lookup the student in UNI DB.

Usage:
  python3 backend/app/ocr_lookup.py /path/to/card.jpg

Requires UNI DB env vars in backend/.env.
"""

import sys
from pathlib import Path

import cv2
from dotenv import load_dotenv

# Add project root to sys.path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from computer_vision import scan_student_id_card
from backend.app.crud import lookup_uni_student


def main() -> None:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(env_path)
    if len(sys.argv) < 2:
        print("Usage: python3 backend/app/ocr_lookup.py /path/to/card.jpg")
        return

    image_path = Path(sys.argv[1])
    if not image_path.exists():
        print(f"Image not found: {image_path}")
        return

    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Failed to load image: {image_path}")
        return

    result = scan_student_id_card(image)
    print("OCR result:", result)

    if not result.get("success"):
        print("OCR failed; no database lookup performed.")
        return

    student_id = result.get("student_id")
    if not student_id:
        print("OCR success without student_id; no database lookup performed.")
        return

    student = lookup_uni_student(student_id)
    if student is None:
        print("Student not found in UNI DB.")
        return

    print("Student record:")
    for key, value in student.items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
