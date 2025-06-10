import numpy as np
import cv2

def adjust_contrast_by_range(imageBGRA, inRange, outRange, mask=None):
    """
    Adjusts the contrast of the given image by applying a linear transformation to the V channel of the image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        inRange (tuple): The input range for the V channel of the image.
        outRange (tuple): The output range for the V channel of the image.
        mask (numpy.ndarray): A mask to apply the contrast adjustment only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with adjusted contrast in the BGRA format.
    """
    imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)      # convert the image to HSV color space
    
    # calculate params and apply the contrast adjustment to the V channel
    alpha = (outRange[1] - outRange[0]) / (inRange[1] - inRange[0])
    beta = outRange[0] - (alpha * inRange[0])
    enhanced = cv2.convertScaleAbs(imageHSV[:, :, 2], -1, alpha, beta) 

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSV[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSV[:, :, 2])

    imageBGRA[:, :, :3] = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)               # convert back to BGRA color space

    return imageBGRA