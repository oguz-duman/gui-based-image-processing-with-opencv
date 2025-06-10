from app import utils
import numpy as np
import cv2

def add_poisson_noise(imageBGRA, mask=None):
    """
    Applies Poisson noise to the input image.
    Args:
        imageBGRA (numpy.ndarray): Input image in BGRA format.
        mask (numpy.ndarray): A mask to apply the noise only to certain pixels.
    Returns:
        numpy.ndarray: The resulting image with Poisson noise applied, in BGRA format.
    """
    imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)      # convert the BGRA image to BGR color space

    # If the image is grayscale, make the noise channels identical
    if utils.is_image_grayscale(imageBGRA):
        imageGray = np.random.poisson(imageBGR[:, :, 0].astype(np.float32))
        imageBGR = cv2.merge((imageGray, imageGray, imageGray))
    else:
        imageBGR = np.random.poisson(imageBGR.astype(np.float32))

    # If a mask is provided, use it to update only the pixels where mask != 0
    mask3 = None if mask is None else mask[:, :, np.newaxis]                # expand the mask dimensions to match the noise shape
    imageBGR = imageBGR if mask3 is None else np.where(mask3 > 0, imageBGR, imageBGRA[:, :, :3])
    
    imageBGR = np.clip(imageBGR, 0, 255).astype(np.uint8)       # clip the values to the range [0, 255]
    imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       # set back the alpha channel to make it BGRA

    return imageBGRA