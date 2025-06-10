from app import utils
import numpy as np
import cv2

def adjust_brightness(imageBGRA, value, mask=None):
    """
    Brightens the given image by adding a value to the V channel of the image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        value (int): The value to be added to the V channel of the image.
        mask (numpy.ndarray): A mask to apply the brightness only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The brightened image in the BGRA format.
    """
    imageHSVA = utils.bgra2hsva_transform(imageBGRA)                           # convert the image to HSVA color space
    brightened = cv2.add(imageHSVA[:, :, 2], value)                 # brighten the V channel of the HSVA image

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSVA[:, :, 2] = brightened if mask is None else np.where(mask > 0, brightened, imageHSVA[:, :, 2])
    
    imageBGRA = utils.hsva2bgra_transform(imageHSVA)                           # convert back to BGRA color space

    return imageBGRA