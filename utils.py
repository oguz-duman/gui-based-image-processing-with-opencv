import cv2
from PySide6.QtWidgets import QFileDialog, QMessageBox


def select_image():
    # Open file dialog to select an image file
    filePath, _ = QFileDialog.getOpenFileName(None, "Select an image file", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp)")

    # Check if a file was selected
    if filePath:
        image = cv2.imread(filePath, cv2.IMREAD_UNCHANGED)      # read the image
        
        if image is None:
            raise ValueError("No input image provided")
        elif len(image.shape) == 2:  # if image is  (h,w)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)
        elif len(image.shape) == 3 and image.shape[2] == 1:  # if image is (h,w,1)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)
        elif len(image.shape) == 3 and image.shape[2] == 3:  # ig image is (BGR) (h,w,3)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        elif len(image.shape) == 3 and image.shape[2] == 4:  # if image is (BGRA) (h,w,4)
            pass
        else:
            raise ValueError("Unsupported image format")
        
        return image
        

def save_image(image):
    """
    Open a file dialog to save the output image.
    """
    # Open file dialog to select a file path to save the image
    filePath, _ = QFileDialog.getSaveFileName(None, "Save the image", "", "Image Files (*.jpg *.jpeg *.png *.bmp *.gif *.tif *.tiff *.webp)")
    
    # Check if a file path was selected
    if filePath:
        try:
            cv2.imwrite(filePath, image)            # Save the image using OpenCV
        except:
            QMessageBox.information(None, "Error", f"Failed to save the image. Please try again.")



