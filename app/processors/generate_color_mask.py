from app import utils
import numpy as np
import cv2

def generate_color_mask(imageBGRA, lowerBound, upperBound, invert=False):
    """
    Applies a mask to the given image based on the specified lower and upper bounds.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        lowerBound, upperBound (tuple): The lower and upper bounds for the mask in the HSVA color space.
    Returns:
        imageBGRA (numpy.ndarray): The masked image in the BGRA format.
    """
    imageHSVA = utils.bgra2hsva_transform(imageBGRA)                           # convert the image to HSVA color space
    mask = cv2.inRange(imageHSVA[:, :, :3], lowerBound, upperBound) # create a mask based on the range values
    mask = cv2.bitwise_not(mask) if invert else mask                # Invert the mask if 'invert' is True

    return mask