import sys
from pathlib import Path

import cv2

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from computer_vision import scan_student_id_card


def main():
    image_path = "computer_vision/data/test_cards/sample_1.jpg"
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return

    result = scan_student_id_card(image)
    print(result)


if __name__ == "__main__":
    main()
