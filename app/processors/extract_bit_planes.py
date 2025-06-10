import numpy as np
import cv2

def extract_bit_planes(imageBGRA, bitPlane):
    """
    Extracts the specified bit plane from the given image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        bitPlane (int): The bit plane to be extracted from the image. The value should be between 0 and 7.
    Returns:
        imageBGRA (numpy.ndarray): The image with the specified bit plane extracted in the BGRA format.
    """
    imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)   # convert the image to HSV color space
    imageGray = cv2.bitwise_and(imageHSV[:, :, 2], 1 << bitPlane)    # get the selected bit plane using V channel
    imageBinary = np.where(imageGray > 0, 255, 0).astype(np.uint8)    # convert the bit plane to binary image
    imageBGR = cv2.cvtColor(imageBinary, cv2.COLOR_GRAY2BGR)          # make the binary image 3 channel
    imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))             # set back the alpha channel to make it BGRA
    
    return imageBGRA