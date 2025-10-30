"""
Tiền xử lý ảnh cho nhận diện biển số xe – OpenCV
File này được gọi từ Java bằng ProcessBuilder
"""

import argparse
from pathlib import Path
import cv2
import numpy as np
import math

# -------------------------
# Utilities
# -------------------------
def imread_color(path: str | Path) -> np.ndarray:
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Không đọc được ảnh: {path}")
    return img


def detect_plate_region(bgr: np.ndarray):
    # chuyển sang ảnh xám
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 3))
    blackhat = cv2.morphologyEx(gray_blur, cv2.MORPH_BLACKHAT, rect_kernel)

    gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=3)
    gradX = cv2.convertScaleAbs(gradX)
    gradX = cv2.normalize(gradX, None, 0, 255, cv2.NORM_MINMAX)

    _, thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 5))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, close_kernel, iterations=2)
    closed = cv2.morphologyEx(
        closed, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    )

    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    H, W = gray.shape[:2]
    candidates = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        aspect = w / (h + 1e-6)
        fill_ratio = cv2.contourArea(cnt) / (area + 1e-6)

        if 2.0 < aspect < 8.5 and area > 0.002 * (W * H) and fill_ratio > 0.4:
            candidates.append(((x, y, w, h), fill_ratio, area))

    if not candidates:
        return None

    candidates.sort(key=lambda it: (it[1], it[2]), reverse=True)
    (x, y, w, h), _, _ = candidates[0]
    return (x, y, w, h)


def crop_with_padding(img: np.ndarray, box, pad: int = 6) -> np.ndarray:
    x, y, w, h = box
    H, W = img.shape[:2]
    x0 = max(0, x - pad)
    y0 = max(0, y - pad)
    x1 = min(W, x + w + pad)
    y1 = min(H, y + h + pad)
    return img[y0:y1, x0:x1]


# -------------------------
# Main
# -------------------------
def main():
    parser = argparse.ArgumentParser(description="Nhận diện biển số xe")
    parser.add_argument("image", help="Đường dẫn ảnh đầu vào (ảnh xe)")
    parser.add_argument("output", help="Đường dẫn ảnh kết quả (biển số đã cắt)")
    args = parser.parse_args()

    img_path = Path(args.image)
    out_path = Path(args.output)

    bgr = imread_color(img_path)
    box = detect_plate_region(bgr)

    if box is not None:
        plate_roi = crop_with_padding(bgr, box, pad=8)
        cv2.imwrite(str(out_path), plate_roi)
        print(f"Biển số đã được cắt và lưu tại: {out_path}")
    else:
        cv2.imwrite(str(out_path), bgr)
        print("Không tìm thấy biển số trong ảnh")


if __name__ == "__main__":
    main()
