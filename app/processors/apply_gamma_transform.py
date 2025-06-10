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
    imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)      # convert the image to HSV color space
    vChannel = imageHSV[:, :, 2].astype(np.float32) / 255.0    # get the V channel of the HSVA image
    vChannel = cv2.pow(vChannel, gamma)                         # apply gamma transformation
    enhanced = (vChannel*255).astype(np.uint8)        # update the V channel of the HSVA image
    
    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSV[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSV[:, :, 2])

    imageBGRA[:, :, :3] = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)               # convert back to BGRA color space


    return imageBGRA