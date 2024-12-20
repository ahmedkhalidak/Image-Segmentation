import cv2 as cv
import matplotlib.pyplot as plt
import random
import numpy as np


class AddNoise:
    def __init__(self, image_path):
        self.image_path = image_path
        self.process_image()

    def salt_and_pepper_noise(self, img, amount=0.04):
        noisy_img = img.copy()
        total_pixels = img.size
        num_salt = int(total_pixels * amount / 2)
        num_pepper = int(total_pixels * amount / 2)


        coords = [random.randint(0, i - 1) for i in img.shape]
        for _ in range(num_salt):
            y, x = random.randint(0, img.shape[0] - 1), random.randint(0, img.shape[1] - 1)
            noisy_img[y, x] = 255

 
        for _ in range(num_pepper):
            y, x = random.randint(0, img.shape[0] - 1), random.randint(0, img.shape[1] - 1)
            noisy_img[y, x] = 0

        return noisy_img

    def impulse_noise(self, img, amount=0.02):
        noisy_img = img.copy()
        num_noisy_pixels = int(img.size * amount)

        for _ in range(num_noisy_pixels):
            y, x = random.randint(0, img.shape[0] - 1), random.randint(0, img.shape[1] - 1)
            noisy_img[y, x] = random.choice([0, 255])

        return noisy_img

    def gaussian_noise(self, img, mean=0, sigma=20):
     
        gaussian_noise = np.random.normal(mean, sigma, img.shape).astype(np.uint8)
        noisy_img = cv.add(img, gaussian_noise)
        return noisy_img

    def process_image(self):
        img = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE)
        if img is None:
            print("Error: Failed to load image.")
            return


        salt_pepper_img = self.salt_and_pepper_noise(img)
        impulse_img = self.impulse_noise(img)
        gaussian_img = self.gaussian_noise(img)


        plt.figure(figsize=(15, 15))


        plt.subplot(2, 2, 1)
        plt.imshow(img, cmap='gray')
        plt.axis('off')
        plt.title("Original Image")


        plt.subplot(2, 2, 2)
        plt.imshow(salt_pepper_img, cmap='gray')
        plt.axis('off')
        plt.title("Salt and Pepper Noise")

 
        plt.subplot(2, 2, 3)
        plt.imshow(impulse_img, cmap='gray')
        plt.axis('off')
        plt.title("Impulse Noise")

     
        plt.subplot(2, 2, 4)
        plt.imshow(gaussian_img, cmap='gray')
        plt.axis('off')
        plt.title("Gaussian Noise")


        plt.show()
