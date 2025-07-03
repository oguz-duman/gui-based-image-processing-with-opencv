import cv2
import numpy as np

def generate_color_mask(imageBGRA, lowerBound, upperBound, invert=False, prev_mask=None):
    """
    Applies a mask to the given image based on the specified lower and upper bounds.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        lowerBound, upperBound (tuple): The lower and upper bounds for the mask in the HSVA color space.
    Returns:
        imageBGRA (numpy.ndarray): The masked image in the BGRA format.
    """
    imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)     # convert the image to HSV color space
    mask = cv2.inRange(imageHSV[:, :, :3], lowerBound, upperBound)      # create a mask based on the range values

    # If a mask is provided (this means double masking) apply mask only where the previous mask is not 0 
    mask = mask if prev_mask is None else np.where(prev_mask > 0, mask, 0)    

    mask = cv2.bitwise_not(mask) if invert else mask                    # Invert the mask if 'invert' is True

    return mask