# preprocess.py
import sys
import cv2
import numpy as np
import os

def enhance_image(in_path, out_path, gamma=0.5):
    img = cv2.imread(in_path)
    if img is None:
        print("ERROR: Không đọc được ảnh:", in_path)
        sys.exit(2)

    # BGR -> RGB for processing (we will save as BGR)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Gamma correction
    look_up = np.array([((i / 255.0) ** gamma) * 255 for i in range(256)]).astype("uint8")
    gamma_corrected = cv2.LUT(img, look_up)

    # CLAHE
    lab = cv2.cvtColor(gamma_corrected, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    clahe_img = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)

    # Denoise + sharpening
    denoised = cv2.GaussianBlur(clahe_img, (3, 3), 0)
    gaussian = cv2.GaussianBlur(denoised, (9, 9), 10.0)
    sharpened = cv2.addWeighted(denoised, 1.5, gaussian, -0.5, 0)

    # Save result (convert back to BGR)
    cv2.imwrite(out_path, cv2.cvtColor(sharpened, cv2.COLOR_RGB2BGR))
    print("OK: saved", out_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python preprocess.py <input> <output>")
        sys.exit(1)
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    enhance_image(in_path, out_path)
