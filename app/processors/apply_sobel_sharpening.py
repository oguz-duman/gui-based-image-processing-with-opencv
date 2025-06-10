from app import processor_utils
import numpy as np
import cv2

def apply_sobel_sharpening(imageBGRA, alpha, mask=None):
    """
    Applies Sobel sharpening to the V channel of the given image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        alpha (float): The scaling factor for the V channel of the image.
        mask (numpy.ndarray): A mask to apply the Sobel sharpening only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with Sobel sharpening applied in the BGRA format.
    """
    # create the sobel kernels
    w_x = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
    w_y = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)

    imageHSVA = processor_utils.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
    vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image
    vChannel = vChannel.astype(np.float32) / 255.0              # normalize the image to 0-1 range

    # apply sobel kernel on x axis
    laplace_x = cv2.filter2D(vChannel, cv2.CV_32F, w_x, borderType=cv2.BORDER_REPLICATE)  
    vChannel = vChannel + laplace_x * alpha                     # sharpen the image using the sobel filter

    # apply sobel kernel on y axis
    laplace_y = cv2.filter2D(vChannel, cv2.CV_32F, w_y, borderType=cv2.BORDER_REPLICATE)  
    vChannel = vChannel + laplace_y * alpha                     # sharpen the image using the sobel filter
    vChannel = np.clip(vChannel, 0, 1)                          # clip the image to 0-1 range
    vChannel = (vChannel * 255).astype(np.uint8)                # convert back to uint8

    # If a mask is provided, use it to update only the pixels where mask != 0
    imageHSVA[:, :, 2] = vChannel if mask is None else np.where(mask > 0, vChannel, imageHSVA[:, :, 2])

    imageBGRA = processor_utils.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

    return imageBGRA