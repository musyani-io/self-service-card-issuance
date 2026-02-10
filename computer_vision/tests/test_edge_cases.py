import sys
from pathlib import Path
import importlib.util

import numpy as np

# Resolve computer_vision root and load config directly from file
CV_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = CV_ROOT / "config" / "ocr_config.py"

if str(CV_ROOT) not in sys.path:
    sys.path.insert(0, str(CV_ROOT))

if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

spec = importlib.util.spec_from_file_location("ocr_config", CONFIG_PATH)
ocr_config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ocr_config)

from pipeline.ocr_pipeline import CardOCRPipeline


def run_case(name: str, image):
    pipeline = CardOCRPipeline(ocr_config.__dict__)
    result = pipeline.scan_card(image)
    status = "✅" if result["success"] else "⚠️"
    print(f"{status} {name}: {result}")


def main():
    cases = {}

    # Empty / None input
    cases["none_image"] = None

    # Empty array
    cases["empty_array"] = np.array([])

    # Very small image
    cases["tiny_50x50"] = np.zeros((50, 50, 3), dtype=np.uint8)

    # Wrong format (grayscale)
    cases["grayscale"] = np.zeros((200, 300), dtype=np.uint8)

    # Random noise
    cases["noise_300x200"] = np.random.randint(0, 255, (200, 300, 3), dtype=np.uint8)

    # Solid bright
    cases["white_300x200"] = np.full((200, 300, 3), 255, dtype=np.uint8)

    # Solid dark
    cases["black_300x200"] = np.zeros((200, 300, 3), dtype=np.uint8)

    for name, image in cases.items():
        try:
            run_case(name, image)
        except Exception as exc:
            print(f"❌ {name}: Exception: {exc}")


if __name__ == "__main__":
    main()
