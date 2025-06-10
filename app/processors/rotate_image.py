from app.processors.apply_padding import apply_padding
from app.processors.crop_image import crop_image
import numpy as np
import cv2

def rotate_image(imageBGRA, angle):
    """
    Rotates the given image by the specified angle.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        angle (float): The angle by which to rotate the image.
    Returns:
        imageBGRA (numpy.ndarray): The rotated image in the BGRA format.
    """
    # get the shape of the image and calculate the center
    (h, w) = imageBGRA.shape[:2]
    center = (w / 2, h / 2)

    # calculate the needed padding to avoid cropping after rotation
    max_x = w * abs(np.cos(np.radians(angle))) + h * abs(np.sin(np.radians(angle)))
    max_y = w * abs(np.sin(np.radians(angle))) + h * abs(np.cos(np.radians(angle)))
    pad_w = int(np.ceil(max_x - w))
    pad_h = int(np.ceil(max_y - h))

    # calculate the cut values to crop the image after rotation to avoid unnecessary paddings
    cut_x = -pad_w if pad_w < 0 else 0
    cut_y = -pad_h if pad_h < 0 else 0

    # prevent negative padding values
    pad_w = 0 if pad_w < 0 else pad_w
    pad_h = 0 if pad_h < 0 else pad_h

    # apply padding to the image before rotation
    imageBGRA = apply_padding(imageBGRA, cv2.BORDER_CONSTANT, pad_w//2, pad_w//2, pad_h//2, pad_h//2, (0, 0, 0, 0))  
    
    # recalculate the shape and center after padding
    (h, w) = imageBGRA.shape[:2]
    center = (w / 2, h / 2)

    # rotate the image around the center
    M = cv2.getRotationMatrix2D(center, angle, 1)
    imageBGRA = cv2.warpAffine(imageBGRA, M, (w, h))

    # crop the image to remove the unnecessary paddings
    imageBGRA = crop_image(imageBGRA, cut_x//2, cut_x//2, cut_y//2, cut_y//2)

    return imageBGRA