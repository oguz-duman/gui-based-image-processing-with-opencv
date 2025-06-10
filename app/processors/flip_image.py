import cv2

def flip_image(imageBGRA, flipCode):
    """
    Flips the given image based on the provided flip code.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        flipCode (int): The flip code for the image. 0 for vertical flip, 1 for horizontal flip, -1 for both.
    Returns:
        imageBGRA (numpy.ndarray): The flipped image in the BGRA format.
    """
    imageBGRA = cv2.flip(imageBGRA, flipCode)       # flip the image based on the provided flip code

    return imageBGRA