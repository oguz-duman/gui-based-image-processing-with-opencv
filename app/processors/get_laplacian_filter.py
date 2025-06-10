from app import utils
import numpy as np
import cv2

def get_laplacian_filter(imageBGRA, extended=False, normalize=False):
    """
    Applies Laplacian filter to the V channel of the given image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        extended (bool): If True, use extended Laplacian kernel. Default is False.
        normalize (bool): If True, normalize the filtered image. Default is False.
    Returns:
        imageBGRA (numpy.ndarray): The image with Laplacian filter applied in the BGRA format.
    """
    # create the laplace kernel according to the extended switch
    if extended:
        w = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
    else:
        w = np.array([[0, 1, 0], [0, -4, 0], [0, 1, 0]], dtype=np.float32)

    imageHSVA = utils.bgra2hsva_transform(imageBGRA)                                       # convert the image to HSVA color space
    vChannel = imageHSVA[:, :, 2].astype(np.float32) / 255.0                    # get the V channel of the HSVA image
    laplace = cv2.filter2D(vChannel, -1, w, borderType=cv2.BORDER_REPLICATE)    # apply the laplace filter to the V channel

    # normalize the filtered image if the normalize switch is checked
    if normalize:
        laplace = cv2.normalize(laplace, None, 0, 1, cv2.NORM_MINMAX)
    
    laplace = (np.clip(laplace, 0, 1) * 255).astype(np.uint8)                   # clip the values to the range [0, 255]  
    imageBGR = cv2.cvtColor(laplace, cv2.COLOR_GRAY2BGR)                        # mkae the laplace image 3 channel
    imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))                       # set back the alpha channel to make it BGRA
    
    return imageBGRA