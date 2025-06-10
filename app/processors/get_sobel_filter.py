import numpy as np
import cv2


def get_sobel_filter(imageBGRA, normalize=False):
    """
    Applies Sobel filter to the V channel of the given image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        normalize (bool): If True, normalize the filtered image. Default is False.
        mask (numpy.ndarray): A mask to apply the Sobel filter only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The image with Sobel filter applied in the BGRA format.
    """
    # create the sobel kernels
    w_x = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
    w_y = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)

    imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)     # convert the image to HSV color space
    vChannel = imageHSV[:, :, 2].astype(np.float32) / 255.0             # get and normalize the V channel of the HSVA image

    # get the sobel filters
    sobel_x = cv2.filter2D(vChannel, -1, w_x, borderType=cv2.BORDER_REPLICATE)
    sobel_y = cv2.filter2D(vChannel, -1, w_y, borderType=cv2.BORDER_REPLICATE)
    sobel = np.sqrt(sobel_x ** 2 + sobel_y ** 2)

    # normalize the filtered image if the normalize switch is checked
    if normalize:
        sobel = cv2.normalize(sobel, None, 0, 1, cv2.NORM_MINMAX)

    sobel = (np.clip(sobel, 0, 1) * 255).astype(np.uint8)       # clip the values to the range [0, 255]
    imageBGR = cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR)          # mkae the sobel image 3 channel
    imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       # set back the alpha channel of the image
    
    return imageBGRA