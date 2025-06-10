from app import utils
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
    imageHSVA = utils.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
    
    # calculate params and apply the contrast adjustment to the V channel
    alpha = (outRange[1] - outRange[0]) / (inRange[1] - inRange[0])
    beta = outRange[0] - (alpha * inRange[0])
    enhanced = cv2.convertScaleAbs(imageHSVA[:, :, 2], -1, alpha, beta) 

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSVA[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSVA[:, :, 2])


    imageBGRA = utils.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

    return imageBGRA