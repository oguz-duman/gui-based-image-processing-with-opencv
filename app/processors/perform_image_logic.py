from app import utils
import numpy as np
import cv2

def perform_image_logic(imageBGRA, secondImage, operation):
    """
    Performs logical operations on the given image and a second image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        secondImage (numpy.ndarray): The second image to perform logical operations with.
        operation (str): The logical operation to be performed. Options are "And", "Or", "Xor".
    Returns:
        imageBGRA (numpy.ndarray): The resulting image after the logical operation in the BGRA format.
    """
    imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)              # convert the BGRA image to BGR color space
    
    # resize the second image to match the size of the first image
    secondImage = cv2.resize(secondImage, (imageBGRA.shape[1], imageBGRA.shape[0]))  
    
    # perform the selected arithmetic operation    
    if operation == "And":
        imageBGR = cv2.bitwise_and(imageBGR, secondImage)
    elif operation == "Or":
        imageBGR = cv2.bitwise_or(imageBGR, secondImage)
    elif operation == "Xor":
        imageBGR = cv2.bitwise_xor(imageBGR, secondImage)

    imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))               # set back the alpha channel to make it BGRA

    return imageBGRA