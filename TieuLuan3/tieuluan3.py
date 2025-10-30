# -*- coding: utf-8 -*-
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from sklearn.cluster import KMeans
class SegmentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Segmentation Application - Python")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f2f4f5")

        self.img = None
        self.result = None

        # ====== FRAME CHÍNH ======
        self.left_frame = tk.Frame(self.root, bg="#dfe6e9", width=600, height=550)
        self.left_frame.pack(side="left", padx=10, pady=10)
        self.left_frame.pack_propagate(False)

        self.right_frame = tk.Frame(self.root, bg="#ecf0f1", width=350, height=550)
        self.right_frame.pack(side="right", padx=10, pady=10)
        self.right_frame.pack_propagate(False)

        # ====== ẢNH HIỂN THỊ ======
        self.lbl_image = tk.Label(self.left_frame, text="No image loaded", bg="#dfe6e9", font=("Arial", 12))
        self.lbl_image.pack(expand=True)

        # ====== BẢNG NÚT CHỨC NĂNG ======
        self.build_right_panel()

    # ==========================================================
    def build_right_panel(self):
        tk.Label(self.right_frame, text="Controls", bg="#ecf0f1", font=("Arial", 14, "bold")).pack(pady=5)

        btn_frame = tk.Frame(self.right_frame, bg="#ecf0f1")
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Load Image", command=self.load_image).grid(row=0, column=0, padx=3)
        ttk.Button(btn_frame, text="Save Image", command=self.save_image).grid(row=0, column=1, padx=3)
        ttk.Button(btn_frame, text="Reset", command=self.reset_image).grid(row=0, column=2, padx=3)

        ttk.Separator(self.right_frame, orient='horizontal').pack(fill="x", pady=10)

        # --- Khu vực chọn lĩnh vực ---
        tk.Label(self.right_frame, text="Select Domain:", bg="#ecf0f1", font=("Arial", 11, "bold")).pack()
        self.combo = ttk.Combobox(self.right_frame, values=[
            "Y tế – Tách khối u MRI (Watershed cải tiến)",
            "Nông nghiệp – Đếm số quả",
            "Giao thông – Phát hiện vạch đường",
            "An ninh – Tách người khỏi nền"
        ], state="readonly", width=35)
        self.combo.pack(pady=5)
        self.combo.set("Y tế – Tách khối u MRI (Watershed cải tiến)")

        ttk.Button(self.right_frame, text="▶ Run Segmentation", command=self.run_segmentation).pack(pady=10)

        ttk.Separator(self.right_frame, orient='horizontal').pack(fill="x", pady=10)
        self.status = tk.Label(self.right_frame, text="Ready", bg="#ecf0f1", fg="#2d3436", font=("Arial", 10, "italic"))
        self.status.pack(side="bottom", pady=10)

    # ==========================================================
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg;*.bmp")])
        if file_path:
            self.img = cv2.imread(file_path)
            self.show_image(self.img)
            self.status.config(text="Image loaded successfully ")

    def save_image(self):
        if self.result is None:
            self.status.config(text="No result to save ")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Files", "*.png"), ("JPG Files", "*.jpg")])
        if save_path:
            cv2.imwrite(save_path, self.result)
            self.status.config(text=f"Result saved at {save_path}")

    def reset_image(self):
        if self.img is not None:
            self.show_image(self.img)
            self.result = None
            self.status.config(text="Image reset")

    def show_image(self, cv_img):
        """Hiển thị ảnh trong vùng bên trái."""
        cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(cv_img_rgb)
        im.thumbnail((580, 540))
        imgtk = ImageTk.PhotoImage(image=im)
        self.lbl_image.configure(image=imgtk, text="")
        self.lbl_image.image = imgtk

    # ==========================================================
    def run_segmentation(self):
        def choice_T(img):
            min = np.min(img)
            max = np.max(img)
            T0 = (min+max)//2
            while True:
                g1 = img[img <= T0]
                g2 = img[img > T0]
                u1 = np.mean(g1) if len(g1) > 0 else 0
                u2 = np.mean(g2) if len(g2) > 0 else 0
                Tnew = (u1+u2)//2
                if(np.abs(Tnew - T0) < 0.5):
                    break
                T0 = Tnew
            return T0
        if self.img is None:
            self.status.config(text="No image loaded ")
            return

        option = self.combo.get()
        img = self.img.copy()
        result = None

        # --- Y tế: Watershed cải tiến ---
        if "MRI" in option:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Tăng tương phản bằng CLAHE
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)

            # Làm mờ giảm nhiễu
            blur = cv2.GaussianBlur(enhanced, (5,5), 0)

            # Ngưỡng Otsu
            _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Đảo ngược nếu vùng sáng chiếm đa số
            if np.sum(binary == 255) > np.sum(binary == 0):
                binary = cv2.bitwise_not(binary)

            kernel = np.ones((3,3), np.uint8)
            morph = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)

            # Distance transform để tìm vùng chắc chắn
            dist_transform = cv2.distanceTransform(morph, cv2.DIST_L2, 5)
            _, sure_fg = cv2.threshold(dist_transform, 0.6 * dist_transform.max(), 255, 0)
            sure_fg = np.uint8(sure_fg)
            sure_bg = cv2.dilate(morph, kernel, iterations=3)
            unknown = cv2.subtract(sure_bg, sure_fg)

            # Marker và watershed
            _, markers = cv2.connectedComponents(sure_fg)
            markers = markers + 1
            markers[unknown == 255] = 0
            cv2.watershed(img, markers)

            # ======= TÔ VÙNG KHỐI U =======
            mask = np.zeros_like(gray)
            mask[markers == 2] = 255  # vùng foreground chính

            # Lấy contour lớn nhất (vì vùng u thường lớn nhất)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                c = max(contours, key=cv2.contourArea)
                # Tạo lớp tô màu (overlay)
                overlay = img.copy()
                cv2.drawContours(overlay, contours, -1, (0, 0, 255), -1)  # tô vùng u bằng đỏ đặc
                # Pha trộn overlay với ảnh gốc để tạo hiệu ứng bán trong suốt
                result = cv2.addWeighted(img, 0.7, overlay, 0.3, 0)
            else:
                result = cv2.bitwise_and()

            self.status.config(text="MRI tumor detected successfully ")


        # --- Nông nghiệp ---
        elif "quả" in option:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, (10, 100, 20), (30, 255, 255))
            cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            result = img.copy()
            cv2.drawContours(result, cnts, -1, (0, 255, 0), 2)
            cv2.putText(result, f"So qua: {len(cnts)}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            self.status.config(text=f"Detected {len(cnts)} fruits ")

        # --- Giao thông ---
        elif "đường" in option:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 1)
            edges = cv2.Canny(blur, 230, 255)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=100, maxLineGap=50)
            result = img.copy()
            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(result, (x1, y1), (x2, y2), (0,255,0), 3)
            self.status.config(text="Lane detection done ")

        # --- An ninh ---
        elif "nền" in option:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Tính ngưỡng động
            T = choice_T(gray)
            _, th = cv2.threshold(gray, T, 255, cv2.THRESH_BINARY)
            print(T)
            # Đảo ngược nếu cần (tùy ảnh nền sáng hay tối)
            if np.sum(th == 255) > np.sum(th == 0):
                th = cv2.bitwise_not(th)
            
            # Áp mask lên ảnh gốc để tách vùng foreground
            result = cv2.bitwise_and(img, img, mask=th)

            self.status.config(text="Background removed ")
        if result is not None:
            self.result = result
            self.show_image(result)

# ==========================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = SegmentationApp(root)
    root.mainloop()
