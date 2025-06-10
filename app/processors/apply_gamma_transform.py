from app import processor_utils
import numpy as np
import cv2

def apply_gamma_transform(imageBGRA, gamma, mask=None):
    """
    Adjusts the contrast of the given image by applying gamma transformation to the V channel of the image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        gamma (float): The gamma value for the transformation.
        mask (numpy.ndarray): A mask to apply the contrast adjustment only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with adjusted contrast in the BGRA format.
    """
    imageHSVA = processor_utils.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
    vChannel = imageHSVA[:, :, 2].astype(np.float32) / 255.0    # get the V channel of the HSVA image
    vChannel = cv2.pow(vChannel, gamma)                         # apply gamma transformation
    enhanced = (vChannel*255).astype(np.uint8)        # update the V channel of the HSVA image
    
    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSVA[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSVA[:, :, 2])

    imageBGRA = processor_utils.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

    return imageBGRA