import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np
import random
import matplotlib.pyplot as plt

class GalleryApp:
    def __init__(self, parent):
        self.parent = parent
        self.image_size = (400, 300)
        self.original_image = None
        self.processed_image = None
        self.image_path = None
        self.history = []

        self.content_frame = tk.Frame(self.parent, bg="#FFFFFF")
        self.content_frame.pack(pady=10, fill="both")

        self.img_label = tk.Label(self.content_frame, text="No image loaded", font=("Arial", 16), bg="#FFFFFF")
        self.img_label.pack(pady=20)

        self.buttons_frame = tk.Frame(self.parent)
        self.buttons_frame.pack(pady=10)

        self.btn_load_image = tk.Button(self.buttons_frame, text="Load Image", command=self.load_image)
        self.btn_load_image.pack(side="left", padx=10)

        self.btn_noise = tk.Button(self.buttons_frame, text="Add Noise", command=self.add_noise, font=("Arial", 12, "bold"), bg="#176782", fg="white")
        self.btn_noise.pack(side="left", padx=10)

        self.btn_remove_noise = tk.Button(self.buttons_frame, text="Remove Noise", command=self.remove_noise, font=("Arial", 12, "bold"), bg="#176782", fg="white")
        self.btn_remove_noise.pack(side="left", padx=10)

        self.btn_histogram = tk.Button(self.buttons_frame, text="Histogram Equalization", command=self.histogram_eq, font=("Arial", 12, "bold"), bg="#176782", fg="white")
        self.btn_histogram.pack(side="left", padx=10)

        self.btn_sobel = tk.Button(self.buttons_frame, text="Sobel Edge Detection", command=self.sobel_edge, font=("Arial", 12, "bold"), bg="#176782", fg="white")
        self.btn_sobel.pack(side="left", padx=10)

        self.btn_prewitt = tk.Button(self.buttons_frame, text="Prewitt Edge Detection", command=self.prewitt_edge, font=("Arial", 12, "bold"), bg="#176782", fg="white")
        self.btn_prewitt.pack(side="left", padx=10)

        self.btn_laplacian = tk.Button(self.buttons_frame, text="Laplacian of Gaussian", command=self.laplacian_of_gaussian, font=("Arial", 12, "bold"), bg="#176782", fg="white")
        self.btn_laplacian.pack(side="left", padx=10)

        self.bottom_buttons_frame = tk.Frame(self.parent)
        self.bottom_buttons_frame.pack(pady=10)

        self.btn_reset = tk.Button(self.bottom_buttons_frame, text="Reset", command=self.reset_image, font=("Arial", 12, "bold"), bg="#E74C3C", fg="white")
        self.btn_reset.pack(side="left", padx=10)

        self.btn_save = tk.Button(self.bottom_buttons_frame, text="Save Image", command=self.save_image, font=("Arial", 12, "bold"), bg="#2ECC71", fg="white")
        self.btn_save.pack(side="left", padx=10)

        self.btn_undo = tk.Button(self.bottom_buttons_frame, text="Undo", command=self.undo, font=("Arial", 12, "bold"), bg="#F39C12", fg="white")
        self.btn_undo.pack(side="left", padx=10)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path
            self.original_image = cv.imread(file_path, cv.IMREAD_GRAYSCALE)
            if self.original_image is None:
                messagebox.showerror("Error", "Failed to load image")
                return
            self.processed_image = self.original_image.copy()
            self.history = [self.processed_image.copy()]
            self.update_image()

    def update_image(self):
        if self.processed_image is not None:
            try:
                image = Image.fromarray(self.processed_image)
                image = image.resize(self.image_size)
                photo = ImageTk.PhotoImage(image)

                self.img_label.config(image=photo, text="")
                self.img_label.image = photo
            except Exception as e:
                messagebox.showerror("Error", f"Could not display image: {e}")
        else:
            self.img_label.config(text="No image loaded", image="")

    def salt_and_pepper_noise(self, img, amount=0.04):
        noisy_img = img.copy()
        total_pixels = img.size
        num_salt = int(total_pixels * amount / 2)
        num_pepper = int(total_pixels * amount / 2)

        for _ in range(num_salt):
            y, x = random.randint(0, img.shape[0] - 1), random.randint(0, img.shape[1] - 1)
            noisy_img[y, x] = 255

        for _ in range(num_pepper):
            y, x = random.randint(0, img.shape[0] - 1), random.randint(0, img.shape[1] - 1)
            noisy_img[y, x] = 0

        return noisy_img

    def add_noise(self):
        if self.original_image is None:
            messagebox.showerror("Error", "No image loaded.")
            return
        noisy_image = self.salt_and_pepper_noise(self.original_image)
        self.processed_image = noisy_image
        self.history.append(self.processed_image.copy())
        self.update_image()

    def remove_noise(self):
        if self.processed_image is None:
            messagebox.showerror("Error", "No noisy image to remove.")
            return
        denoised_image = self.remove_medianBlur(self.processed_image)
        self.processed_image = denoised_image
        self.history.append(self.processed_image.copy())
        self.update_image()

    def remove_medianBlur(self, img):
        return cv.medianBlur(img, 5)

    def histogram_eq(self):
        if self.processed_image is None:
            messagebox.showerror("Error", "No image loaded.")
            return
        histo_original = cv.calcHist([self.original_image], [0], None, [256], [0, 256])
        hist_eq_image = cv.equalizeHist(self.processed_image)
        self.processed_image = hist_eq_image
        histo_eq = cv.calcHist([self.processed_image], [0], None, [256], [0, 256])

        plt.figure(figsize=(10, 8))

        plt.subplot(2, 1, 1)
        plt.title("Original Image Histogram")
        plt.plot(histo_original)
        plt.xlim([0, 256])

        plt.subplot(2, 1, 2)
        plt.title("Equalized Image Histogram")
        plt.plot(histo_eq)
        plt.xlim([0, 256])

        plt.tight_layout()
        plt.show()

        self.history.append(self.processed_image.copy())
        self.update_image()

    def prewitt_edge(self):
        if self.processed_image is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])

        gradient_x = cv.filter2D(self.processed_image, -1, kernel_x)
        gradient_y = cv.filter2D(self.processed_image, -1, kernel_y)

        gradient_x = gradient_x.astype(np.float64)
        gradient_y = gradient_y.astype(np.float64)

        prewitt_edge = cv.magnitude(gradient_x, gradient_y)

        self.processed_image = prewitt_edge
        self.update_image()

    def sobel_edge(self):
        if self.processed_image is None:
            messagebox.showerror("Error", "No image loaded.")
            return
        sobel_x = cv.Sobel(self.processed_image, cv.CV_64F, 1, 0, ksize=3)
        sobel_y = cv.Sobel(self.processed_image, cv.CV_64F, 0, 1, ksize=3)
        sobel_edge = cv.magnitude(sobel_x, sobel_y)
        self.processed_image = sobel_edge
        self.history.append(self.processed_image.copy())
        self.update_image()

    def laplacian_of_gaussian(self):
        if self.processed_image is None:
            messagebox.showerror("Error", "No image loaded.")
            return

      
        blurred_image = cv.GaussianBlur(self.processed_image, (5, 5), 0)
        

        log_image = cv.Laplacian(blurred_image, cv.CV_64F)
        
  
        log_image_abs = np.absolute(log_image)


        log_image_normalized = np.uint8(log_image_abs / np.max(log_image_abs) * 255)


        self.processed_image = log_image_normalized
        self.update_image()

    def reset_image(self):
        if self.original_image is None:
            messagebox.showerror("Error", "No image loaded.")
            return
        self.processed_image = self.original_image.copy()
        self.history = [self.processed_image.copy()]
        self.update_image()

    def save_image(self):
        if self.processed_image is None:
            messagebox.showerror("Error", "No image to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
        if file_path:
            cv.imwrite(file_path, self.processed_image)
            messagebox.showinfo("Info", "Image saved successfully!")

    def undo(self):
        if len(self.history) > 1:
            self.history.pop()
            self.processed_image = self.history[-1]
            self.update_image()
        else:
            messagebox.showinfo("Info", "No more actions to undo.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GalleryApp(root)
    root.mainloop()
