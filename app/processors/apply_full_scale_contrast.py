from app import processor_utils
import numpy as np
import cv2

def apply_full_scale_contrast(imageBGRA, mask=None):
    """
    Adjusts the contrast of the given image by applying full scale contrast stretching to the V channel of the image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        mask (numpy.ndarray): A mask to apply the contrast adjustment only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with adjusted contrast in the BGRA format.
    """
    imageHSVA = processor_utils.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space

    # perform full scale contrast stretching
    enhanced = cv2.normalize(imageHSVA[:, :, 2], None, 0, 255, cv2.NORM_MINMAX)

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSVA[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSVA[:, :, 2])

    imageBGRA = processor_utils.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

    return imageBGRA