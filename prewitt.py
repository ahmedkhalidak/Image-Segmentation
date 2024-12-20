import cv2
import numpy as np
import matplotlib.pyplot as plt


class Prewitt:
    def __init__(self, image_path):
        self.image_path = image_path
        self.process_image()

    def process_image(self):
        image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            print("Error: Failed to load image.")
            return
        kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        prewitt_x = cv2.filter2D(image, -1, kernel_x)
        prewitt_y = cv2.filter2D(image, -1, kernel_y)
        prewitt = cv2.magnitude(prewitt_x.astype(np.float64), prewitt_y.astype(np.float64))

     
        plt.figure(figsize=(10, 6))
        
        plt.subplot(2, 2, 1)
        plt.title('Original Image')
        plt.imshow(image, cmap='gray')


        plt.subplot(2,2,2)
        plt.title('Prewitt Edge Detection')
        plt.imshow(prewitt, cmap='gray')

        plt.tight_layout()
        plt.show()    
        
                
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt


class Prewitt:
    def __init__(self, image_path):
        self.image_path = image_path
        self.process_image()

    def process_image(self):
        
        image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print("Error: Failed to load image.")
            return

        
        kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])

       
        rows, cols = image.shape

        
        prewitt_x = np.zeros_like(image, dtype=np.float64)
        prewitt_y = np.zeros_like(image, dtype=np.float64)
        prewitt = np.zeros_like(image, dtype=np.float64)

       
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                
                region = image[i - 1:i + 2, j - 1:j + 2]

                
                gx = np.sum(kernel_x * region)

                
                gy = np.sum(kernel_y * region)

                
                prewitt_x[i, j] = gx
                prewitt_y[i, j] = gy

                
                prewitt[i, j] = np.sqrt(gx**2 + gy**2)

        # عرض النتائج
        plt.figure(figsize=(10, 6))

        plt.subplot(2, 2, 1)
        plt.title('Original Image')
        plt.imshow(image, cmap='gray')

        plt.subplot(2, 2, 2)
        plt.title('Prewitt X')
        plt.imshow(prewitt_x, cmap='gray')

        plt.subplot(2, 2, 3)
        plt.title('Prewitt Y')
        plt.imshow(prewitt_y, cmap='gray')

        plt.subplot(2, 2, 4)
        plt.title('Prewitt Edge Detection')
        plt.imshow(prewitt, cmap='gray')

        plt.tight_layout()
        plt.show()


prewitt_filter = Prewitt("path_to_your_image.jpg")


"""