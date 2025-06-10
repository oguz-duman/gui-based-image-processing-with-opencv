from app import utils
import numpy as np
import cv2

def add_salt_and_pepper(imageBGRA, saltPepProb, mask=None):
    """
    Adds salt and pepper noise to the given image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        saltPepProb (float): The probability of salt and pepper noise to be added to the image.
        mask (numpy.ndarray): A mask to apply the noise only to certain pixels.
    Returns 
        imageBGRA (numpy.ndarray): The image with salt and pepper noise added in the BGRA format.
    """
    imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)          # convert the BGRA image to BGR color space
    numSalt = int(imageBGR.size * saltPepProb)                      # number of salt pixels to add
    numPep = int(imageBGR.size * saltPepProb)                       # number of pepper pixels to add

    # generate random coordinates for salt and pepper noise
    saltCoords = [np.random.randint(0, i-1, numSalt) for i in imageBGR.shape]
    pepCoords = [np.random.randint(0, i-1, numPep) for i in imageBGR.shape]
    
    imageBGR[saltCoords[0], saltCoords[1]] = [255, 255, 255]    # add salt noise
    imageBGR[pepCoords[0], pepCoords[1]] = [0,0,0]              # add pepper noise


    # If a mask is provided, use it to update only the pixels where mask != 0
    mask3 = None if mask is None else mask[:, :, np.newaxis]                # Expand the mask dimensions to match the noise shape
    imageBGR = imageBGR if mask3 is None else np.where(mask3 > 0, imageBGR, imageBGRA[:, :, :3])

    imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       # set back the alpha channel to make it BGRA
    
    return imageBGRA 