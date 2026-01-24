import cv2
from pathlib import Path
from computer_vision.core.image_utils import convert_to_grayscale

BASE_DIR = Path(__file__).resolve().parents[1]
sample_path = BASE_DIR / "data" / "sample_barcodes" / "IMG-20260120-WA0037.jpg"
output_dir = BASE_DIR / "data" / "debug_outputs"
output_dir.mkdir(parents=True, exist_ok=True)

color = cv2.imread(str(sample_path))
if color is None:
    raise FileNotFoundError(f"Could not find image at {sample_path}")

gray = convert_to_grayscale(color)

gray_output = output_dir / "test1.jpg"
cv2.imwrite(str(gray_output), gray)