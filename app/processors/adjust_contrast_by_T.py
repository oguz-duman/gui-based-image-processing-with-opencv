import numpy as np
import cv2

def adjust_contrast_by_T(imageBGRA, alpha, beta, mask=None):
    """
    Adjusts the contrast of the given image by applying a linear transformation to the V channel of the image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        alpha (float): The scaling factor for the V channel of the image.
        beta (int): The offset value for the V channel of the image.
        mask (numpy.ndarray): A mask to apply the contrast adjustment only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with adjusted contrast in the BGRA format.
    """
    imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)      # convert the image to HSV color space

    # apply the contrast adjustment to the v channel of the HSVA image
    enhanced = cv2.convertScaleAbs(imageHSV[:, :, 2], -1, alpha, beta) 

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSV[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSV[:, :, 2])

    imageBGRA[:, :, :3] = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)               # convert back to BGRA color space

    return imageBGRA