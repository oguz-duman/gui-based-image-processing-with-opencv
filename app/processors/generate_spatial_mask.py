import numpy as np
import cv2


def generate_spatial_mask(imageBGRA, width, height, left, top, border_radius, invert=False):
    """
    Creates a spatial mask to be used by other image processing functions.
    Args:
        imageBGRA (numpy.ndarray): The input image in the BGRA format.
        width (int): The width of the mask.
        height (int): The height of the mask.
        left (int): The x-coordinate of the top-left corner of the mask.
        top (int): The y-coordinate of the top-left corner of the mask.
        border_radius (int): The radius of the border for the mask.
    Returns:
        imageBGRA (numpy.ndarray): The image with the spatial mask applied in the BGRA format.
        Inside the mask, the image will be same, outside the mask, the image will be black.
    """
    (im_height, im_width) = imageBGRA.shape[:2]                 # get the width and height of the image

    # make sure parameters are not out of bounds
    left = max(0, min(im_width - width, left))                              
    top = max(0, min(im_height - height, top))          
    border_radius = min(border_radius, width // 2, height // 2)     

    mask = np.zeros((im_height, im_width), dtype=np.uint8)

    # Create submask with rounded corners
    submask = np.zeros((height, width), dtype=np.uint8)

    # --- Super-sampling factor ---
    scale = 16
    large_width = width * scale
    large_height = height * scale
    large_radius = border_radius * scale

    # Create high-res submask
    submask_large = np.zeros((large_height, large_width), dtype=np.uint8)

    # Draw rectangles
    cv2.rectangle(submask_large, (large_radius, 0), (large_width - large_radius, large_height), 255, -1)
    cv2.rectangle(submask_large, (0, large_radius), (large_width, large_height - large_radius), 255, -1)

    # Draw rounded corners
    cv2.ellipse(submask_large, (large_radius, large_radius), (large_radius, large_radius), 180, 0, 90, 255, -1)
    cv2.ellipse(submask_large, (large_width - large_radius, large_radius), (large_radius, large_radius), 270, 0, 90, 255, -1)
    cv2.ellipse(submask_large, (large_width - large_radius, large_height - large_radius), (large_radius, large_radius), 0, 0, 90, 255, -1)
    cv2.ellipse(submask_large, (large_radius, large_height - large_radius), (large_radius, large_radius), 90, 0, 90, 255, -1)

    # Downsample to original size (anti-aliasing effect)
    submask = cv2.resize(submask_large, (width, height), interpolation=cv2.INTER_AREA)

    # Ensure binary mask (0 or 255)
    _, submask = cv2.threshold(submask, 127, 255, cv2.THRESH_BINARY)

    mask[top:top+height, left:left+width] = submask         # Place on full mask

    mask = cv2.bitwise_not(mask) if invert else mask        # Invert the mask if 'invert' is True

    return mask