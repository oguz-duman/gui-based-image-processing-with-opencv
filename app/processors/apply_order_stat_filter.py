import numpy as np
import cv2


def apply_order_stat_filter(imageBGRA, kernelSize, order, mask=None):
    """
    Applies order statistics filter to the V channel of the given image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        kernelSize (int): The size of the kernel for the filter.
        order (str): The order statistic to be applied. Options are "max", "min", "median".
        mask (numpy.ndarray): A mask to apply the filter only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with order statistics filter applied in the BGRA format.
    """
    imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)      # convert the image to HSV color space

    # apply the order statistics filter to the V channel
    if order == "max":
        filtered = cv2.dilate(imageHSV[:, :, 2], np.ones((kernelSize, kernelSize), np.uint8), borderType=cv2.BORDER_REPLICATE)   
    elif order == "min":
        filtered = cv2.erode(imageHSV[:, :, 2], np.ones((kernelSize, kernelSize), np.uint8),borderType=cv2.BORDER_REPLICATE)     
    elif order == "median":
        filtered = cv2.medianBlur(imageHSV[:, :, 2], kernelSize)  

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSV[:, :, 2] = filtered if mask is None else np.where(mask > 0, filtered, imageHSV[:, :, 2])

    imageBGRA[:, :, :3] = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)               # convert back to BGRA color space

    return imageBGRA