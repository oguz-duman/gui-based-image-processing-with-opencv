from app import utils
import numpy as np
import cv2

def apply_log_transform(imageBGRA, mask=None):
    """
    Adjusts the contrast of the given image by applying log transformation to the V channel of the image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        mask (numpy.ndarray): A mask to apply the contrast adjustment only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with adjusted contrast in the BGRA format.
    """        
    imageHSVA = utils.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
    vChannel = imageHSVA[:, :, 2].astype(np.float32)            # get the V channel of the HSVA image
    vChannel = np.log(1 + vChannel)                             # apply log transformation
    vChannel = cv2.normalize(vChannel, None, 0, 255, cv2.NORM_MINMAX)
    enhanced = vChannel.astype(np.uint8)              # update the V channel of the HSVA image

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSVA[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSVA[:, :, 2])

    imageBGRA = utils.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

    return imageBGRA