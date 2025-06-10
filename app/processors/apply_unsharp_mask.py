from app import processor_utils
import numpy as np
import cv2

def apply_unsharp_mask(imageBGRA, kernelSize, sigma, alpha, mask=None):
    """
    Applies unsharp masking to the V channel of the given image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        kernelSize (int): The size of the kernel for the filter.
        sigma (float): The standard deviation for the Gaussian kernel.
        alpha (float): The scaling factor for the V channel of the image.
        mask (numpy.ndarray): A mask to apply the unsharp masking only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with unsharp masking applied in the BGRA format.
    """
    imageHSVA = processor_utils.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
    vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image
    vChannel = vChannel.astype(np.float32) / 255.0              # normalize the image to 0-1 range

    Blurred = cv2.GaussianBlur(vChannel, (kernelSize, kernelSize), sigma, borderType=cv2.BORDER_REPLICATE)     
    Sharp = vChannel - Blurred                                  # get the sharpened filter
    vChannel = vChannel + Sharp * alpha                         # sharpen the image
    vChannel = np.clip(vChannel, 0, 1)                          # clip the image to 0-1 range
    vChannel = (vChannel * 255).astype(np.uint8)                # convert back to uint8

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSVA[:, :, 2] = vChannel if mask is None else np.where(mask > 0, vChannel, imageHSVA[:, :, 2])

    imageBGRA = processor_utils.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

    return imageBGRA