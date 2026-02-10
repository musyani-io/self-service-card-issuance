"""
Interactive ROI calibration tool.

Usage:
  python3 computer_vision/tools/roi_calibrator.py /path/to/card.jpg

Draw rectangles for each ROI. Press:
  - n: next ROI
  - r: reset current ROI
  - s: save and exit
"""

import sys
from pathlib import Path
import json
import cv2
import tkinter as tk

ROI_KEYS = ["name", "student_id", "program", "expiry_date"]


def to_ratio(rect, width, height):
    x, y, w, h = rect
    return {
        "x_start": x / width,
        "x_end": (x + w) / width,
        "y_start": y / height,
        "y_end": (y + h) / height,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 computer_vision/tools/roi_calibrator.py /path/to/card.jpg")
        return

    image_path = Path(sys.argv[1])
    if not image_path.exists():
        print(f"Image not found: {image_path}")
        return

    image = cv2.imread(str(image_path))
    if image is None:
        print("Failed to load image")
        return

    height, width = image.shape[:2]

    # Compute scale to fit screen
    root = tk.Tk()
    root.withdraw()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    root.destroy()

    max_w = int(screen_w * 0.9)
    max_h = int(screen_h * 0.9)
    scale = min(max_w / width, max_h / height, 1.0)

    if scale < 1.0:
        disp_w = int(width * scale)
        disp_h = int(height * scale)
        display_image = cv2.resize(image, (disp_w, disp_h), interpolation=cv2.INTER_AREA)
    else:
        display_image = image
        disp_w, disp_h = width, height
    rois = {}
    idx = 0

    try:
        while idx < len(ROI_KEYS):
            key = ROI_KEYS[idx]
            clone = display_image.copy()
            cv2.putText(
                clone,
                f"Draw ROI for: {key} (Enter/Space to accept, c to cancel)",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )
            cv2.namedWindow("ROI Calibrator", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("ROI Calibrator", disp_w, disp_h)
            rect = cv2.selectROI(
                "ROI Calibrator", clone, fromCenter=False, showCrosshair=True
            )
            cv2.destroyWindow("ROI Calibrator")

            if rect == (0, 0, 0, 0):
                print(f"No ROI selected for {key}")
            else:
                # Map rect from display scale to original image coordinates
                x, y, w, h = rect
                if scale != 1.0:
                    x = int(x / scale)
                    y = int(y / scale)
                    w = int(w / scale)
                    h = int(h / scale)

                rois[key] = to_ratio((x, y, w, h), width, height)
                print(f"Captured {key}: {rois[key]}")

            action = input("Enter n=next, r=redo, s=save, q=quit: ").strip().lower()
            if action == "s":
                idx = len(ROI_KEYS)
            elif action == "q":
                print("Exiting without saving.")
                return
            elif action == "r":
                continue
            else:
                idx += 1
    finally:
        cv2.destroyAllWindows()

    output = {"ROIS": rois}
    print("\nROI output (ratios):")
    print(json.dumps(output, indent=2))

    out_path = image_path.with_suffix(".rois.json")
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"Saved ROI config to: {out_path}")


if __name__ == "__main__":
    main()
