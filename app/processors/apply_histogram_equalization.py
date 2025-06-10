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
    imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)      # convert the image to HSV color space

    enhanced = cv2.equalizeHist(imageHSV[:, :, 2])       # equalize the V channel of the HSVA image
    
    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSV[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSV[:, :, 2])
    
    imageBGRA[:, :, :3] = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)               # convert back to BGRA color space

    
    return imageBGRA