import numpy as np
import cv2

def apply_image_arithmetic(imageBGRA, secondImage, alpha, operation):
    """
    Performs arithmetic operations on the given image and a second image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        secondImage (numpy.ndarray): The second image to perform arithmetic operations with.
        alpha (float): The alpha value for the operation.
        operation (str): The arithmetic operation to be performed. Options are "Add", "Subtract", "Multiply", "Divide".
    Returns:
        imageBGRA (numpy.ndarray): The resulting image after the arithmetic operation in the BGRA format.
    """
    imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR).astype(np.float32)  # convert the BGRA image to BGR color space
    
    # resize the second image to match the size of the first image and multiply with alpha
    secondImage = cv2.resize(secondImage, (imageBGRA.shape[1], imageBGRA.shape[0])).astype(np.float32) * alpha  
    
    # perform the selected arithmetic operation    
    if operation == "Add":
        imageBGR = cv2.add(imageBGR, secondImage)
    elif operation == "Subtract":
        imageBGR = cv2.subtract(imageBGR, secondImage)
    elif operation == "Multiply":
        imageBGR = cv2.multiply(imageBGR, secondImage)
    elif operation == "Divide":
        imageBGR = cv2.divide(imageBGR, secondImage + 1e-10)

    imageBGR = np.clip(imageBGR, 0, 255).astype(np.uint8)       # clip the values to the range [0, 255]
    imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       # set back the alpha channel to make it BGRA

    return imageBGRA