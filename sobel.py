import cv2
import numpy as np
import matplotlib.pyplot as plt


class Sobel:
    def __init__(self, image_path):
        self.image_path = image_path
        self.process_image()

    def process_image(self):
        image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            print("Error: Failed to load image.")
            return


        sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        sobel = cv2.magnitude(sobel_x, sobel_y)




        plt.figure(figsize=(10, 6))
        plt.subplot(2, 2, 1)
        plt.title('Original Image')
        plt.imshow(image, cmap='gray')

        plt.subplot(2, 2, 2)
        plt.title('Sobel Edge Detection')
        plt.imshow(sobel, cmap='gray')



        plt.tight_layout()
        plt.show()
        
        
"""


class Sobel:
  
    def __init__(self, image_path):
        self.image_path = image_path
        self.process_image()

    def process_image(self):
       
        image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print("Error: Failed to load image.")
            return

        
        sobel_x_kernel = np.array([[-1, 0, 1], 
                                   [-2, 0, 2], 
                                   [-1, 0, 1]])  # Gradient in x
        sobel_y_kernel = np.array([[1, 2, 1], 
                                   [0, 0, 0], 
                                   [-1, -2, -1]])  # Gradient in y

     
        rows, cols = image.shape
        sobel_x = np.zeros((rows, cols), dtype=np.float64)
        sobel_y = np.zeros((rows, cols), dtype=np.float64)

     
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                
                region = image[i-1:i+2, j-1:j+2]

           
                sobel_x[i, j] = np.sum(region * sobel_x_kernel)
                sobel_y[i, j] = np.sum(region * sobel_y_kernel)

        sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

        
        sobel_magnitude = (sobel_magnitude / sobel_magnitude.max()) * 255
        sobel_magnitude = sobel_magnitude.astype(np.uint8)

       
        plt.figure(figsize=(10, 6))

        plt.subplot(1, 3, 1)
        plt.title('Original Image')
        plt.imshow(image, cmap='gray')

        plt.subplot(1, 3, 2)
        plt.title('Sobel X Gradient')
        plt.imshow(np.abs(sobel_x), cmap='gray')

        plt.subplot(1, 3, 3)
        plt.title('Sobel Y Gradient')
        plt.imshow(np.abs(sobel_y), cmap='gray')

        plt.figure(figsize=(6, 6))
        plt.title('Sobel Edge Detection')
        plt.imshow(sobel_magnitude, cmap='gray')

        plt.tight_layout()
        plt.show()
"""