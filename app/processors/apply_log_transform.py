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
    imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)      # convert the image to HSV color space

    vChannel = imageHSV[:, :, 2].astype(np.float32)            # get the V channel of the HSVA image
    vChannel = np.log(1 + vChannel)                             # apply log transformation
    vChannel = cv2.normalize(vChannel, None, 0, 255, cv2.NORM_MINMAX)
    enhanced = vChannel.astype(np.uint8)              # update the V channel of the HSVA image

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSV[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSV[:, :, 2])

    imageBGRA[:, :, :3] = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)               # convert back to BGRA color space

    return imageBGRA