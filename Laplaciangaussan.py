import cv2
import numpy as np
import matplotlib.pyplot as plt


class GaussianAndLaplacianApp:
    def __init__(self, image_path):
        self.image_path = image_path
        self.process_image()

    def gaussian_derivative(self, image, sigma=1.0):
      
        ksize = 5 

        gauss_blur_x = cv2.GaussianBlur(image, (ksize, ksize), sigma)

        kernel_x = np.array([[-1, 0, 1]]) 
        kernel_x_blurred = cv2.filter2D(gauss_blur_x, -1, kernel_x)


        kernel_y = np.array([[-1], [0], [1]]) 
        kernel_y_blurred = cv2.filter2D(gauss_blur_x, -1, kernel_y)

        magnitude = cv2.magnitude(kernel_x_blurred.astype(np.float64), kernel_y_blurred.astype(np.float64))
        
        return magnitude

    def process_image(self):
        

        image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            print("Error: Failed to load image.")
            return


        result = self.gaussian_derivative(image)


        plt.figure(figsize=(10, 6))

        plt.subplot(2, 2, 1)
        plt.title('Original Image')
        plt.imshow(image, cmap='gray')
        plt.axis('off')

        plt.subplot(2, 2, 2)
        plt.title('Gaussian Edge Detection')
        plt.imshow(result, cmap='gray')
        plt.axis('off')

        plt.tight_layout()
        plt.show()



if __name__ == "__main__":
    image_path = 'your_image_path_here.jpg'
    app = GaussianAndLaplacianApp(image_path)
