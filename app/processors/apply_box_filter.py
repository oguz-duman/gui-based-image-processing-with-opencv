import numpy as np
import cv2

def apply_box_filter(imageBGRA, kernelSize, mask=None):
    """
    Applies box filter to the V channel of the given image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        kernelSize (int): The size of the kernel for the filter.
        mask (numpy.ndarray): A mask to apply the box filter only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with box filter applied in the BGRA format.
    """
    imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)      # convert the image to HSV color space

    # apply the box filter to the V channel
    blurred = cv2.blur(imageHSV[:, :, 2], (kernelSize, kernelSize), borderType=cv2.BORDER_REPLICATE)    

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSV[:, :, 2] = blurred if mask is None else np.where(mask > 0, blurred, imageHSV[:, :, 2])

    imageBGRA[:, :, :3] = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)               # convert back to BGRA color space

    return imageBGRA