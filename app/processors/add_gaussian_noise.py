from app import processor_utils
import numpy as np
import cv2

def add_gaussian_noise(imageBGRA, mean, std, mask=None):
    """
    Adds Gaussian noise to the given image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        mean (float): The mean value for the Gaussian noise.
        std (float): The standard deviation for the Gaussian noise.
        mask (numpy.ndarray): A mask to apply the noise only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with Gaussian noise added in the BGRA format.
    """
    imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR).astype(np.float32)          # convert the BGRA image to BGR color space

    # If the image is grayscale, make the noise channels identical
    if processor_utils.is_image_grayscale(imageBGRA):
        noise = np.random.normal(mean, std, imageBGR[:, :, 0].shape).astype(np.float32) 
        noise = cv2.merge((noise, noise, noise))
    else:
        noise = np.random.normal(mean, std, imageBGR.shape).astype(np.float32)

    noised = cv2.add(imageBGR, noise)                                # add noise

    # If a mask is provided, use it to update only the pixels where mask != 0
    mask3 = None if mask is None else mask[:, :, np.newaxis]                # expand the mask dimensions to match the noise shape
    imageBGR = noised if mask3 is None else np.where(mask3 > 0, noised, imageBGR)

    imageBGR = np.clip(imageBGR, 0, 255).astype(np.uint8)       # clip the values to the range [0, 255]
    imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       # set back the alpha channel to make it BGRA
    
    return imageBGRA