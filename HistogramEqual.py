import cv2 as cv
import matplotlib.pyplot as plt

class histogram:
    def __init__(self, image_path):
        self.image_path = image_path
        self.process_image()

    def process_image(self):
        img = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE)

        if img is None:
            print("Error: Failed to load image.")
            return

        
        histo = cv.calcHist([img], [0], None, [256], [0, 256])
        cdf = histo.cumsum()
        cdfNorm = cdf * float(histo.max()) / cdf.max()

        
        equImg = cv.equalizeHist(img)

        
        equhist = cv.calcHist([equImg], [0], None, [256], [0, 256])
        equcdf = equhist.cumsum()
        cdfNorm = equcdf * float(equhist.max()) / equcdf.max()

        
        plt.figure(figsize=(10, 8))

        
        plt.subplot(2, 2, 1)
        plt.imshow(img, cmap='gray')
        plt.title("Original Image")
        plt.axis('off')

        plt.subplot(2, 2, 2)
        plt.plot(histo, color='black')
        plt.title("Histogram of Original Image")

       
        plt.subplot(2, 2, 3)
        plt.imshow(equImg, cmap='gray')
        plt.title("Equalized Image")
        plt.axis('off')

        plt.subplot(2, 2, 4)
        plt.plot(equhist, color='black')
        plt.title("Histogram of Equalized Image")

       
        plt.tight_layout()
        plt.show()
