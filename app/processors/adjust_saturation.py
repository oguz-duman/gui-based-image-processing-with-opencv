from app import processor_utils
import numpy as np
import cv2

def adjust_saturation(imageBGRA, value, color_space, mask=None):
    """
    Adjusts the saturation of the given image by adding a value to the S channel of the image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        value (int): The value to be added to the S channel of the image.
        color_space (str): The color space to which the saturation adjustment should be applied.
        mask (numpy.ndarray): A mask to apply the brightness only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with adjusted saturation in the BGRA format.
    """
    if processor_utils.is_image_grayscale(imageBGRA):
        return imageBGRA

    imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)     # convert the image to HSVA color space
    adjusted = cv2.add(imageHSV[:, :, 1], value)                        # adjust the S channel of the HSVA image
    
    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSV[:, :, 1] = adjusted if mask is None else np.where(mask > 0, adjusted, imageHSV[:, :, 1])
    
    imageBGRA[:, :, :3] = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)       # convert back to BGRA color space           

    return imageBGRA