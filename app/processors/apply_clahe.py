from app import utils
import numpy as np
import cv2


def apply_clahe(imageBGRA, clipLimit, tileGridSize, mask=None):
    """
    Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) to the V channel of the given image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        clipLimit (float): The clip limit for the CLAHE algorithm.
        tileGridSize (int): The size of the grid for the CLAHE algorithm.
        mask (numpy.ndarray): A mask to apply the CLAHE only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with CLAHE applied in the BGRA format.
    """
    imageHSVA = utils.bgra2hsva_transform(imageBGRA)                           # convert the image to HSVA color space
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(tileGridSize, tileGridSize))
    enhanced = clahe.apply(imageHSVA[:, :, 2])            # apply CLAHE to the V channel of the HSVA image

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSVA[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSVA[:, :, 2])

    imageBGRA = utils.hsva2bgra_transform(imageHSVA)                           # convert back to BGRA color space
    
    return imageBGRA