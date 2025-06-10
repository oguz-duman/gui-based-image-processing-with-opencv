from app import processor_utils
import numpy as np
import cv2

def adjust_saturation(imageBGRA, value, mask=None):
    """
    Adjusts the saturation of the given image by adding a value to the S channel of the image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        value (int): The value to be added to the S channel of the image.
        mask (numpy.ndarray): A mask to apply the brightness only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with adjusted saturation in the BGRA format.
    """
    if not processor_utils.is_image_grayscale(imageBGRA):
        imageHSVA = processor_utils.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
        saturated = cv2.add(imageHSVA[:, :, 1], value)     # adjust the S channel of the HSVA image

        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSVA[:, :, 1] = saturated if mask is None else np.where(mask > 0, saturated, imageHSVA[:, :, 1])

        imageBGRA = processor_utils.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

    return imageBGRA