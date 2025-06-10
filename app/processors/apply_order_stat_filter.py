from app import processor_utils
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
    imageHSVA = processor_utils.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
    vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image

    # apply the order statistics filter to the V channel
    if order == "max":
        vChannel = cv2.dilate(vChannel, np.ones((kernelSize, kernelSize), np.uint8), borderType=cv2.BORDER_REPLICATE)   
    elif order == "min":
        vChannel = cv2.erode(vChannel, np.ones((kernelSize, kernelSize), np.uint8),borderType=cv2.BORDER_REPLICATE)     
    elif order == "median":
        vChannel = cv2.medianBlur(vChannel, kernelSize)  

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSVA[:, :, 2] = vChannel if mask is None else np.where(mask > 0, vChannel, imageHSVA[:, :, 2])

    imageBGRA = processor_utils.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

    return imageBGRA