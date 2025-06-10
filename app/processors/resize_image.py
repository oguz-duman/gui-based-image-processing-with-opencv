import cv2


def resize_image(imageBGRA, newWidth, newHeight, interpolation):
    """
    Resizes the given image to the specified width and height.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        newWidth, newHeight (int): The new width and height of the image.
    Returns:
        imageBGRA (numpy.ndarray): The resized image in the BGRA format.
    """
    if interpolation is None:
        imageBGRA = cv2.resize(imageBGRA, (newWidth, newHeight))       # resize the image to the specified size
    else:
        imageBGRA = cv2.resize(imageBGRA, (newWidth, newHeight), interpolation=interpolation)       # resize the image to the specified size

    return imageBGRA