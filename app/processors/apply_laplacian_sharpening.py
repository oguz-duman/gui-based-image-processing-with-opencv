import numpy as np
import cv2


def apply_laplacian_sharpening(imageBGRA, alpha, extended=False, mask=None):
    """
    Applies Laplacian sharpening to the V channel of the given image.   
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        alpha (float): The scaling factor for the V channel of the image.
        extended (bool): If True, use extended Laplacian kernel. Default is False.
        mask (numpy.ndarray): A mask to apply the Laplacian sharpening only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with Laplacian sharpening applied in the BGRA format.
    """
    # create the laplace kernel
    if extended:
        w = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
    else:
        w = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)

    imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)     # convert the image to HSV color space
    vChannel = imageHSV[:, :, 2].astype(np.float32) / 255.0             # get and normalize the V channel of the HSV image    
    laplace = cv2.filter2D(vChannel, cv2.CV_32F, w, borderType=cv2.BORDER_REPLICATE)   # get the laplacian filter
    vChannel = vChannel - laplace * alpha                       # sharpen the image using the laplacian filter
    vChannel = np.clip(vChannel, 0, 1)                          # clip the image to 0-1 range
    vChannel = (vChannel * 255).astype(np.uint8)                # convert back to uint8

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSV[:, :, 2] = vChannel if mask is None else np.where(mask > 0, vChannel, imageHSV[:, :, 2])

    imageBGRA[:, :, :3] = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)               # convert back to BGRA color space

    return imageBGRA