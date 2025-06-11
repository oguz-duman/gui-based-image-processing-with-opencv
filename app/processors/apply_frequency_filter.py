import numpy as np
import cv2

def apply_frequency_filter(imageBGRA, filter_radius1, filter_type='Low Pass'):
    """
    Applies a frequency domain filter to each color channel of the input BGRA image.
    Args:
        imageBGRA (ndarray): Input image in BGRA format.
        filter_radius1 (int): Radius for low-pass or high-pass filter.
        filter_radius2 (int, optional): Secondary radius for band-pass/band-stop. Defaults to None.
        filter_type (str): Type of filter - 'low' or 'high'.
    Returns:
        ndarray: Filtered image in BGRA format.
    """
    height, width = imageBGRA.shape[:2]
    center = (width // 2, height // 2)

    # Create mask template
    mask = np.zeros((height, width, 2), np.float32)

    # Distance map
    Y, X = np.ogrid[:height, :width]
    distance = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

    if filter_type == 'Low Pass':
        mask[:,:,0] = mask[:,:,1] = (distance <= filter_radius1).astype(np.float32)
    elif filter_type == 'High Pass':
        mask[:,:,0] = mask[:,:,1] = (distance > filter_radius1).astype(np.float32)
    else:
        raise ValueError("filter_type must be 'low' or 'high'")

    filtered_channels = []
    for i in range(3):  # Only B, G, R channels
        # Convert to float32
        ch_float = np.float32(imageBGRA[:, :, i])
        dft = cv2.dft(ch_float, flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)

        # Apply mask in frequency domain
        fshift_filtered = dft_shift * mask

        # Inverse DFT
        f_ishift = np.fft.ifftshift(fshift_filtered)
        img_back = cv2.idft(f_ishift)
        img_back = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])

        # Normalize to 0-255 and convert to uint8
        img_back_norm = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX)
        filtered_channels.append(img_back_norm.astype(np.uint8))


    output_bgr = cv2.merge(filtered_channels)                       # Merge filtered BGR channels
    output_bgra = cv2.merge((output_bgr, imageBGRA[:, :, 3]))           # Preserve original alpha channel

    return output_bgra