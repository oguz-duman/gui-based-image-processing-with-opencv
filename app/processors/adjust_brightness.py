import numpy as np
import cv2

def adjust_brightness(imageBGRA, value, color_space="HSV", mask=None):
    """
    Brightens the given image by adding a value to the V channel of the image.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        value (int): The value to be added to the V channel of the image.
        color_space (str): The color space to which the brightness adjustment should be applied.
        mask (numpy.ndarray): A mask to apply the brightness only to certain pixels.
    Returns:
        imageBGRA (numpy.ndarray): The brightened image in the BGRA format.
    """
    if color_space == "HSV":
        imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)     # convert the image to HSVA color space
        brightened = cv2.add(imageHSV[:, :, 2], value)                      # brighten the V channel of the HSVA image
        
        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSV[:, :, 2] = brightened if mask is None else np.where(mask > 0, brightened, imageHSV[:, :, 2])
    
        imageBGRA[:, :, :3] = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)      # convert back to BGRA color space

    elif color_space == "RGB":
        brightened =  cv2.add(imageBGRA[:, :, :3], value)
        
        # If a mask is provided, use it to update only the pixels where mask != 0
        imageBGRA[:, :, :3] = brightened if mask is None else np.where(mask > 0, brightened, imageBGRA[:, :, :3])    

    elif color_space == "LAB":
        imageLAB = cv2.cvtColor(imageBGRA[:,:,:3], cv2.COLOR_BGR2LAB)   # convert the image to LAB color space
        brightened = cv2.add(imageLAB[:, :, 0], value)                  # brighten the L channel of the LAB image
        
        # If a mask is provided, use it to update only the pixels where mask != 0
        imageLAB[:, :, 0] = brightened if mask is None else np.where(mask > 0, brightened, imageLAB[:, :, 0])
        
        imageBGRA[:, :, :3] = cv2.cvtColor(imageLAB, cv2.COLOR_LAB2BGR) # convert back to BGRA color space

    return imageBGRA