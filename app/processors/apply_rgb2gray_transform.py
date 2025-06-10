from app import utils
import numpy as np
import cv2

def apply_rgb2gray_transform(imageBGRA):
    """
    Converts the given image from RGB to grayscale.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
    Returns:
        imageBGRA (numpy.ndarray): The converted image in the BGRA format.
    """
    imageHSVA = utils.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
    gray = imageHSVA[:, :, 2]                                   # get only the V channel of the HSVA image
    grayBGR = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)            # make the binary image 3 channel
    grayBGRA = cv2.merge((grayBGR, imageBGRA[:, :, 3]))         # set back the alpha channel of the image

    return grayBGRA