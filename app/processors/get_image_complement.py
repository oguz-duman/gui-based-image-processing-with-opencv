from app import utils
import numpy as np
import cv2

def get_image_complement(imageBGRA):
    """
    Converts the given image to its complement.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
    Returns:
        imageBGRA (numpy.ndarray): The converted image in the BGRA format.
    """
    imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)          # convert the BGRA image to BGR color space       
    imageBGR = cv2.bitwise_not(imageBGR)                            # apply bitwise not to the BGR image                    
    imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))           # set back the alpha channel to make it BGRA
    
    return imageBGRA