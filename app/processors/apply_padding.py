import cv2

def apply_padding(imageBGRA, paddingType, leftPad, rightPad, topPad, bottomPad, constant):
    """
    Applies padding to the given image based on the specified parameters.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        paddingType (int): cv2 padding type to apply like cv2.BORDER_CONSTANT.
        leftPad, rightPad, topPad, bottomPad (int): Number of pixels to pad on each side.
    Returns:
        imageBGRA (numpy.ndarray): The padded image in the BGRA format.
    """
    imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)          # convert the BGRA image to BGR color space

    # apply padding to the image based on the specified padding type
    if paddingType == cv2.BORDER_CONSTANT:
        constant = (constant, constant, constant, constant) if isinstance(constant, int) else constant
        imageBGR = cv2.copyMakeBorder(imageBGR, topPad, bottomPad, leftPad, rightPad, paddingType, value=constant[:3])  
        imageA = cv2.copyMakeBorder(imageBGRA[:, :, 3], topPad, bottomPad, leftPad, rightPad, cv2.BORDER_CONSTANT, value=constant[3])  
    else:
        imageBGR = cv2.copyMakeBorder(imageBGR, topPad, bottomPad, leftPad, rightPad, paddingType)
        imageA = cv2.copyMakeBorder(imageBGRA[:, :, 3], topPad, bottomPad, leftPad, rightPad, cv2.BORDER_CONSTANT, value=255)

    imageBGRA = cv2.merge((imageBGR, imageA))           # set back the alpha channel to make it BGRA

    return imageBGRA