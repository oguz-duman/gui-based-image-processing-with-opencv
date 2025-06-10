from app import processor_utils
import numpy as np
import cv2

def apply_histogram_equalization(imageBGRA, mask=None):
    """
    Applies histogram equalization to the V channel of the given image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        mask (numpy.ndarray): A mask to apply the histogram equalization only to certain pixels.
    Returns 
        imageBGRA (numpy.ndarray): Histogram equalization applied image in the BGRA format.
    """
    imageHSVA = processor_utils.bgra2hsva_transform(imageBGRA)                           # convert the image to HSVA color space
    enhanced = cv2.equalizeHist(imageHSVA[:, :, 2])       # equalize the V channel of the HSVA image
    
    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSVA[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSVA[:, :, 2])
    
    imageBGRA = processor_utils.hsva2bgra_transform(imageHSVA)                           # convert back to BGRA color space
    
    return imageBGRA