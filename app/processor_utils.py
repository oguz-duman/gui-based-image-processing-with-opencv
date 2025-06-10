import numpy as np

def is_image_grayscale(imageBGRA):
    """
    Helper function to check if the given image is grayscale.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
    Returns:
        isGray (bool): True if the image is grayscale, False otherwise.
    """
    return (np.array_equal(imageBGRA[:, :, 0], imageBGRA[:, :, 1]) and np.array_equal(imageBGRA[:, :, 1], imageBGRA[:, :, 2]))

