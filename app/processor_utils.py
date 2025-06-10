import numpy as np
import cv2

def bgra2hsva_transform(imageBGRA):
    """
    Helper function to convert the given image from BGRA to HSVA color space.
    Args:
        imageBGRA (numpy.ndarray): Input image in the BGRA format.
    Returns:
        imageHSVA (numpy.ndarray): The converted image in the HSVA format.
    """
    imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)        # convert the BGRA image to HSV color space
    imageHSVA = cv2.merge((imageHSV, imageBGRA[:, :, 3]))                  # set the alpha channel to make it HSVA
    return imageHSVA


def hsva2bgra_transform(imageHSVA):
    """
    Helper function to convert the given image from HSVA to BGRA color space.
    Args:
        imageHSVA (numpy.ndarray): Input image in the HSVA format.
    Returns:
        imageBGRA (numpy.ndarray): The converted image in the BGRA format.
    """
    imageBGR = cv2.cvtColor(imageHSVA[:, :, :3], cv2.COLOR_HSV2BGR)         # convert the HSVA image to BGR color space
    imageBGRA = cv2.merge((imageBGR, imageHSVA[:, :, 3]))                   # set the alpha channel to make it BGRA
    return imageBGRA


def is_image_grayscale(imageBGRA):
    """
    Helper function to check if the given image is grayscale.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
    Returns:
        isGray (bool): True if the image is grayscale, False otherwise.
    """
    return (np.array_equal(imageBGRA[:, :, 0], imageBGRA[:, :, 1]) and np.array_equal(imageBGRA[:, :, 1], imageBGRA[:, :, 2]))

