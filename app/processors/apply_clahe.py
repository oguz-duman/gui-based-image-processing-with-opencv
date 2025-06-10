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
    imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)      # convert the image to HSV color space
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(tileGridSize, tileGridSize))
    enhanced = clahe.apply(imageHSV[:, :, 2])            # apply CLAHE to the V channel of the HSVA image

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSV[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSV[:, :, 2])

    imageBGRA[:, :, :3] = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)               # convert back to BGRA color space
    
    return imageBGRA