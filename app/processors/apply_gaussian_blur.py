from app import processor_utils
import numpy as np
import cv2

def apply_gaussian_blur(imageBGRA, kernelSize, sigma, mask=None):
    """
    Applies Gaussian blur to the V channel of the given image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        kernelSize (int): The size of the kernel for the filter.
        sigma (float): The standard deviation for the Gaussian kernel.
        mask (numpy.ndarray): A mask to apply the Gaussian blur only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with Gaussian blur applied in the BGRA format.
    """
    imageHSVA = processor_utils.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
    vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image

    # apply the gaussian blur to the V channel
    vChannel = cv2.GaussianBlur(vChannel, (kernelSize, kernelSize), sigma, borderType=cv2.BORDER_REPLICATE)  
    
    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSVA[:, :, 2] = vChannel if mask is None else np.where(mask > 0, vChannel, imageHSVA[:, :, 2])

    imageBGRA = processor_utils.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

    return imageBGRA