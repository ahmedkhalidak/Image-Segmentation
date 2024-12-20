import cv2 as cv
import matplotlib.pyplot as plt
import random


class RemoveNoise:
   

    def __init__(self, image_path):
        self.image_path = image_path
        self.process_image()

    def remove_gaussian_noise(self, img):
    
        denoised_img = cv.GaussianBlur(img, (5, 5), 0)
        return denoised_img

    def remove_median_noise(self, img):
      
   
        denoised_img = cv.medianBlur(img, 5)
        return denoised_img

    def process_image(self):
      
        img = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE)
        img2 = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE) 

        if img is None:
            print("Error: Failed to load image.")
            return


        gaussian_denoised = self.remove_gaussian_noise(img)

      
        median_denoised = self.remove_median_noise(img)

       
        plt.figure(figsize=(20, 10))

        plt.subplot(1, 3, 1)
        plt.imshow(img2, cmap='gray')
        plt.axis('off')
        plt.title("Original Image")

 
        plt.subplot(1, 3, 2)
        plt.imshow(gaussian_denoised, cmap='gray')
        plt.axis('off')
        plt.title("Gaussian Filter ")

       
        plt.subplot(1, 3, 3)
        plt.imshow(median_denoised, cmap='gray')
        plt.axis('off')
        plt.title("Median Filter ")

       
        plt.show()


# image_path = 'path_to_your_image_here.png' 
# noise_processor = RemoveNoise(image_path)
