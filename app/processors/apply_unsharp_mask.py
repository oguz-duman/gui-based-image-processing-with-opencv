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
    imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)      # convert the image to HSV color space
    vChannel = imageHSV[:, :, 2].astype(np.float32) / 255.0              # get and normalize the v channel to 0-1 range

    Blurred = cv2.GaussianBlur(vChannel, (kernelSize, kernelSize), sigma, borderType=cv2.BORDER_REPLICATE)     
    Sharp = vChannel - Blurred                                  # get the sharpened filter
    vChannel = vChannel + Sharp * alpha                         # sharpen the image
    vChannel = np.clip(vChannel, 0, 1)                          # clip the image to 0-1 range
    vChannel = (vChannel * 255).astype(np.uint8)                # convert back to uint8

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSV[:, :, 2] = vChannel if mask is None else np.where(mask > 0, vChannel, imageHSV[:, :, 2])

    imageBGRA[:, :, :3] = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)               # convert back to BGRA color space

    return imageBGRA