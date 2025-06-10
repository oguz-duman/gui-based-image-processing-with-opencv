from app import utils
import numpy as np
import cv2

def apply_threshold_filter(imageBGRA, threshold):
    """
    Converts the given image to binary using a threshold value.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        threshold (int): The threshold value for the conversion.
    Returns:
        imageBGRA (numpy.ndarray): The converted image in the BGRA format.
    """
    imageHSVA = utils.bgra2hsva_transform(imageBGRA)                               # convert the image to HSVA color space
    gray = imageHSVA[:, :, 2]                                           # get only the V channel of the HSVA image
    imageBW = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1] # convert v channel to binary
    bw_BGR = cv2.cvtColor(imageBW, cv2.COLOR_GRAY2BGR)                  # make the binary image 3 channel
    bw_BGRA = cv2.merge((bw_BGR, imageBGRA[:, :, 3]))                   # set back the alpha channel of the image

    return bw_BGRA