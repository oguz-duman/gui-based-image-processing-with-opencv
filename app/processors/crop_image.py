from app import utils
import numpy as np
import cv2


def crop_image(imageBGRA, leftCut, rightCut, topCut, bottomCut):
    """
    Crops the given image by the specified values.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        leftCut, rightCut, topCut, bottomCut (int): Number of pixels to cut from each side.
    Returns:
        imageBGRA (numpy.ndarray): The cropped image in the BGRA format.
    """
    h, w = imageBGRA.shape[:2]                      # get the height and width of the image

    # if the crop values are valid, crop the image
    if leftCut+rightCut < w or topCut+bottomCut < h:
        imageBGRA =  imageBGRA[topCut:-1-bottomCut, leftCut:-1-rightCut]  

    return imageBGRA