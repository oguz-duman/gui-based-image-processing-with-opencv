import numpy as np
import cv2


class Processor():
    """
    This class provides various image processing methods for images in BGRA format.
    It includes helper methods for color space conversion, brightness, contrast, and other image manipulations.
    The methods are designed to work with images in the BGRA format.
    """

    def bgra2hsva_transform(self, imageBGRA):
        """
        Helper function to convert the given image from BGRA to HSVA color space.
        Args:
            imageBGRA (numpy.ndarray): Input image in the BGRA format.
        Returns:
            imageHSVA (numpy.ndarray): The converted image in the HSVA format.
        """
        imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)        # convert the BGRA image to HSV color space
        imageHSVA = cv2.merge((imageHSV, imageBGRA[:, :, 3]))                  # set the alpha channel to make it HSVA
        return imageHSVA
    

    def hsva2bgra_transform(self, imageHSVA):
        """
        Helper function to convert the given image from HSVA to BGRA color space.
        Args:
            imageHSVA (numpy.ndarray): Input image in the HSVA format.
        Returns:
            imageBGRA (numpy.ndarray): The converted image in the BGRA format.
        """
        imageBGR = cv2.cvtColor(imageHSVA[:, :, :3], cv2.COLOR_HSV2BGR)         # convert the HSVA image to BGR color space
        imageBGRA = cv2.merge((imageBGR, imageHSVA[:, :, 3]))                   # set the alpha channel to make it BGRA
        return imageBGRA
    

    def is_image_grayscale(self, imageBGRA):
        """
        Helper function to check if the given image is grayscale.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
        Returns:
            isGray (bool): True if the image is grayscale, False otherwise.
        """
        return (np.array_equal(imageBGRA[:, :, 0], imageBGRA[:, :, 1]) and np.array_equal(imageBGRA[:, :, 1], imageBGRA[:, :, 2]))


    def adjust_brightness(self, imageBGRA, value, mask=None):
        """
        Brightens the given image by adding a value to the V channel of the image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            value (int): The value to be added to the V channel of the image.
            mask (numpy.ndarray): A mask to apply the brightness only to certain pixels.
        Returns:
            imageBGRA (numpy.ndarray): The brightened image in the BGRA format.
        """
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                           # convert the image to HSVA color space
        brightened = cv2.add(imageHSVA[:, :, 2], value)                 # brighten the V channel of the HSVA image

        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSVA[:, :, 2] = brightened if mask is None else np.where(mask > 0, brightened, imageHSVA[:, :, 2])
        
        imageBGRA = self.hsva2bgra_transform(imageHSVA)                           # convert back to BGRA color space

        return imageBGRA


    def adjust_saturation(self, imageBGRA, value, mask=None):
        """
        Adjusts the saturation of the given image by adding a value to the S channel of the image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            value (int): The value to be added to the S channel of the image.
            mask (numpy.ndarray): A mask to apply the brightness only to certain pixels.
        Returns:
            imageBGRA (numpy.ndarray): The image with adjusted saturation in the BGRA format.
        """
        if not self.is_image_grayscale(imageBGRA):
            imageHSVA = self.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
            saturated = cv2.add(imageHSVA[:, :, 1], value)     # adjust the S channel of the HSVA image

            # If a mask is provided, use it to update only the pixels where mask != 0
            imageHSVA[:, :, 2] = saturated if mask is None else np.where(mask > 0, saturated, imageHSVA[:, :, 2])

            imageBGRA = self.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA
    

    def adjust_contrast_by_range(self, imageBGRA, inRange, outRange, mask=None):
        """
        Adjusts the contrast of the given image by applying a linear transformation to the V channel of the image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            inRange (tuple): The input range for the V channel of the image.
            outRange (tuple): The output range for the V channel of the image.
            mask (numpy.ndarray): A mask to apply the contrast adjustment only to certain pixels.
        Returns:
            imageBGRA (numpy.ndarray): The image with adjusted contrast in the BGRA format.
        """
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
        
        # calculate params and apply the contrast adjustment to the V channel
        alpha = (outRange[1] - outRange[0]) / (inRange[1] - inRange[0])
        beta = outRange[0] - (alpha * inRange[0])
        enhanced = cv2.convertScaleAbs(imageHSVA[:, :, 2], -1, alpha, beta) 

        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSVA[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSVA[:, :, 2])


        imageBGRA = self.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA


    def adjust_contrast_by_T(self, imageBGRA, alpha, beta, mask=None):
        """
        Adjusts the contrast of the given image by applying a linear transformation to the V channel of the image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            alpha (float): The scaling factor for the V channel of the image.
            beta (int): The offset value for the V channel of the image.
            mask (numpy.ndarray): A mask to apply the contrast adjustment only to certain pixels.
        Returns:
            imageBGRA (numpy.ndarray): The image with adjusted contrast in the BGRA format.
        """
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space

        # apply the contrast adjustment to the v channel of the HSVA image
        enhanced = cv2.convertScaleAbs(imageHSVA[:, :, 2], -1, alpha, beta) 

        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSVA[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSVA[:, :, 2])

        imageBGRA = self.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA


    def apply_full_scale_contrast(self, imageBGRA, mask=None):
        """
        Adjusts the contrast of the given image by applying full scale contrast stretching to the V channel of the image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            mask (numpy.ndarray): A mask to apply the contrast adjustment only to certain pixels.
        Returns:
            imageBGRA (numpy.ndarray): The image with adjusted contrast in the BGRA format.
        """
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space

        # perform full scale contrast stretching
        enhanced = cv2.normalize(imageHSVA[:, :, 2], None, 0, 255, cv2.NORM_MINMAX)

        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSVA[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSVA[:, :, 2])

        imageBGRA = self.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA


    def apply_log_transform(self, imageBGRA, mask=None):
        """
        Adjusts the contrast of the given image by applying log transformation to the V channel of the image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            mask (numpy.ndarray): A mask to apply the contrast adjustment only to certain pixels.
        Returns:
            imageBGRA (numpy.ndarray): The image with adjusted contrast in the BGRA format.
        """        
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2].astype(np.float32)            # get the V channel of the HSVA image
        vChannel = np.log(1 + vChannel)                             # apply log transformation
        vChannel = cv2.normalize(vChannel, None, 0, 255, cv2.NORM_MINMAX)
        enhanced = vChannel.astype(np.uint8)              # update the V channel of the HSVA image

        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSVA[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSVA[:, :, 2])

        imageBGRA = self.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA


    def apply_gamma_transform(self, imageBGRA, gamma, mask=None):
        """
        Adjusts the contrast of the given image by applying gamma transformation to the V channel of the image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            gamma (float): The gamma value for the transformation.
            mask (numpy.ndarray): A mask to apply the contrast adjustment only to certain pixels.
        Returns:
            imageBGRA (numpy.ndarray): The image with adjusted contrast in the BGRA format.
        """
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2].astype(np.float32) / 255.0    # get the V channel of the HSVA image
        vChannel = cv2.pow(vChannel, gamma)                         # apply gamma transformation
        enhanced = (vChannel*255).astype(np.uint8)        # update the V channel of the HSVA image
        
        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSVA[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSVA[:, :, 2])

        imageBGRA = self.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA
    

    def apply_rgb2gray_transform(self, imageBGRA):
        """
        Converts the given image from RGB to grayscale.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
        Returns:
            imageBGRA (numpy.ndarray): The converted image in the BGRA format.
        """
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
        gray = imageHSVA[:, :, 2]                                   # get only the V channel of the HSVA image
        grayBGR = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)            # make the binary image 3 channel
        grayBGRA = cv2.merge((grayBGR, imageBGRA[:, :, 3]))         # set back the alpha channel of the image

        return grayBGRA
    

    def apply_threshold_filter(self, imageBGRA, threshold):
        """
        Converts the given image to binary using a threshold value.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            threshold (int): The threshold value for the conversion.
        Returns:
            imageBGRA (numpy.ndarray): The converted image in the BGRA format.
        """
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                               # convert the image to HSVA color space
        gray = imageHSVA[:, :, 2]                                           # get only the V channel of the HSVA image
        imageBW = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1] # convert v channel to binary
        bw_BGR = cv2.cvtColor(imageBW, cv2.COLOR_GRAY2BGR)                  # make the binary image 3 channel
        bw_BGRA = cv2.merge((bw_BGR, imageBGRA[:, :, 3]))                   # set back the alpha channel of the image

        return bw_BGRA


    def get_image_complement(self, imageBGRA):
        """
        Converts the given image to its complement.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
        Returns:
            imageBGRA (numpy.ndarray): The converted image in the BGRA format.
        """
        imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)          # convert the BGRA image to BGR color space       
        imageBGR = cv2.bitwise_not(imageBGR)                            # apply bitwise not to the BGR image                    
        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))           # set back the alpha channel to make it BGRA
        return imageBGRA


    def crop_image(self, imageBGRA, leftCut, rightCut, topCut, bottomCut):
        """
        Crops the given image by the specified values.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            leftCut, rightCut, topCut, bottomCut (int): Number of pixels to cut from each side.
        Returns:
            imageBGRA (numpy.ndarray): The cropped image in the BGRA format.
        """
        h, w = imageBGRA.shape[:2]                      # get the height and width of the image

        # if the crop values are valid, crop the image
        if leftCut+rightCut < w or topCut+bottomCut < h:
            imageBGRA =  imageBGRA[topCut:-1-bottomCut, leftCut:-1-rightCut]  

        return imageBGRA

   
    def flip_image(self, imageBGRA, flipCode):
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


    def rotate_image(self, imageBGRA, angle):
        """
        Rotates the given image by the specified angle.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            angle (float): The angle by which to rotate the image.
        Returns:
            imageBGRA (numpy.ndarray): The rotated image in the BGRA format.
        """
        # get the shape of the image and calculate the center
        (h, w) = imageBGRA.shape[:2]
        center = (w / 2, h / 2)

        # calculate the needed padding to avoid cropping after rotation
        max_x = w * abs(np.cos(np.radians(angle))) + h * abs(np.sin(np.radians(angle)))
        max_y = w * abs(np.sin(np.radians(angle))) + h * abs(np.cos(np.radians(angle)))
        pad_w = int(np.ceil(max_x - w))
        pad_h = int(np.ceil(max_y - h))

        # calculate the cut values to crop the image after rotation to avoid unnecessary paddings
        cut_x = -pad_w if pad_w < 0 else 0
        cut_y = -pad_h if pad_h < 0 else 0

        # prevent negative padding values
        pad_w = 0 if pad_w < 0 else pad_w
        pad_h = 0 if pad_h < 0 else pad_h

        # apply padding to the image before rotation
        imageBGRA = self.apply_padding(imageBGRA, cv2.BORDER_CONSTANT, pad_w//2, pad_w//2, pad_h//2, pad_h//2, (0, 0, 0, 0))  
        
        # recalculate the shape and center after padding
        (h, w) = imageBGRA.shape[:2]
        center = (w / 2, h / 2)
    
        # rotate the image around the center
        M = cv2.getRotationMatrix2D(center, angle, 1)
        imageBGRA = cv2.warpAffine(imageBGRA, M, (w, h))

        # crop the image to remove the unnecessary paddings
        imageBGRA = self.crop_image(imageBGRA, cut_x//2, cut_x//2, cut_y//2, cut_y//2)

        return imageBGRA


    def resize_image(self, imageBGRA, newWidth, newHeight, interpolation):
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


    def apply_padding(self, imageBGRA, paddingType, leftPad, rightPad, topPad, bottomPad, constant):
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
    

    def apply_histogram_equalization(self, imageBGRA, mask=None):
        """
        Applies histogram equalization to the V channel of the given image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            mask (numpy.ndarray): A mask to apply the histogram equalization only to certain pixels.
        Returns 
            imageBGRA (numpy.ndarray): Histogram equalization applied image in the BGRA format.
        """
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                           # convert the image to HSVA color space
        enhanced = cv2.equalizeHist(imageHSVA[:, :, 2])       # equalize the V channel of the HSVA image
        
        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSVA[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSVA[:, :, 2])
        
        imageBGRA = self.hsva2bgra_transform(imageHSVA)                           # convert back to BGRA color space
        return imageBGRA


    def apply_clahe(self, imageBGRA, clipLimit, tileGridSize, mask=None):
        """
        Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) to the V channel of the given image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            clipLimit (float): The clip limit for the CLAHE algorithm.
            tileGridSize (int): The size of the grid for the CLAHE algorithm.
            mask (numpy.ndarray): A mask to apply the CLAHE only to certain pixels.
        Returns:
            imageBGRA (numpy.ndarray): The image with CLAHE applied in the BGRA format.
        """
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                           # convert the image to HSVA color space
        clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(tileGridSize, tileGridSize))
        enhanced = clahe.apply(imageHSVA[:, :, 2])            # apply CLAHE to the V channel of the HSVA image

        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSVA[:, :, 2] = enhanced if mask is None else np.where(mask > 0, enhanced, imageHSVA[:, :, 2])

        imageBGRA = self.hsva2bgra_transform(imageHSVA)                           # convert back to BGRA color space
        return imageBGRA
    

    def generate_color_mask(self, imageBGRA, lowerBound, upperBound, invert=False):
        """
        Applies a mask to the given image based on the specified lower and upper bounds.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            lowerBound, upperBound (tuple): The lower and upper bounds for the mask in the HSVA color space.
        Returns:
            imageBGRA (numpy.ndarray): The masked image in the BGRA format.
        """
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                           # convert the image to HSVA color space
        mask = cv2.inRange(imageHSVA[:, :, :3], lowerBound, upperBound) # create a mask based on the range values
        mask = cv2.bitwise_not(mask) if invert else mask                # Invert the mask if 'invert' is True

        return mask


    def generate_spatial_mask(self, imageBGRA, width, height, left, top, border_radius, invert=False):
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
    

    def extract_bit_planes(self, imageBGRA, bitPlane):
        """
        Extracts the specified bit plane from the given image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            bitPlane (int): The bit plane to be extracted from the image. The value should be between 0 and 7.
        Returns:
            imageBGRA (numpy.ndarray): The image with the specified bit plane extracted in the BGRA format.
        """
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                             # convert the image to HSVA color space
        imageGray = cv2.bitwise_and(imageHSVA[:, :, 2], 1 << bitPlane)    # get the selected bit plane using V channel
        imageBinary = np.where(imageGray > 0, 255, 0).astype(np.uint8)    # convert the bit plane to binary image
        imageBGR = cv2.cvtColor(imageBinary, cv2.COLOR_GRAY2BGR)          # make the binary image 3 channel
        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))             # set back the alpha channel to make it BGRA
        return imageBGRA
    

    def add_gaussian_noise(self, imageBGRA, mean, std, mask=None):
        """
        Adds Gaussian noise to the given image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            mean (float): The mean value for the Gaussian noise.
            std (float): The standard deviation for the Gaussian noise.
            mask (numpy.ndarray): A mask to apply the noise only to certain pixels.
        Returns:
            imageBGRA (numpy.ndarray): The image with Gaussian noise added in the BGRA format.
        """
        imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR).astype(np.float32)          # convert the BGRA image to BGR color space

        # If the image is grayscale, make the noise channels identical
        if self.is_image_grayscale(imageBGRA):
            noise = np.random.normal(mean, std, imageBGR[:, :, 0].shape).astype(np.float32) 
            noise = cv2.merge((noise, noise, noise))
        else:
            noise = np.random.normal(mean, std, imageBGR.shape).astype(np.float32)

        noised = cv2.add(imageBGR, noise)                                # add noise

        # If a mask is provided, use it to update only the pixels where mask != 0
        mask3 = None if mask is None else mask[:, :, np.newaxis]                # expand the mask dimensions to match the noise shape
        imageBGR = noised if mask3 is None else np.where(mask3 > 0, noised, imageBGR)

        imageBGR = np.clip(imageBGR, 0, 255).astype(np.uint8)       # clip the values to the range [0, 255]
        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       # set back the alpha channel to make it BGRA
        
        return imageBGRA


    def add_salt_and_pepper(self, imageBGRA, saltPepProb, mask=None):
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


    def add_poisson_noise(self, imageBGRA, mask=None):
        """
        Applies Poisson noise to the input image.
        Args:
            imageBGRA (numpy.ndarray): Input image in BGRA format.
            mask (numpy.ndarray): A mask to apply the noise only to certain pixels.
        Returns:
            numpy.ndarray: The resulting image with Poisson noise applied, in BGRA format.
        """
        imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)      # convert the BGRA image to BGR color space

        # If the image is grayscale, make the noise channels identical
        if self.is_image_grayscale(imageBGRA):
            imageGray = np.random.poisson(imageBGR[:, :, 0].astype(np.float32))
            imageBGR = cv2.merge((imageGray, imageGray, imageGray))
        else:
            imageBGR = np.random.poisson(imageBGR.astype(np.float32))

        # If a mask is provided, use it to update only the pixels where mask != 0
        mask3 = None if mask is None else mask[:, :, np.newaxis]                # expand the mask dimensions to match the noise shape
        imageBGR = imageBGR if mask3 is None else np.where(mask3 > 0, imageBGR, imageBGRA[:, :, :3])
        
        imageBGR = np.clip(imageBGR, 0, 255).astype(np.uint8)       # clip the values to the range [0, 255]
        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       # set back the alpha channel to make it BGRA

        return imageBGRA


    def apply_image_arithmetic(self, imageBGRA, secondImage, alpha, operation):
        """
        Performs arithmetic operations on the given image and a second image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            secondImage (numpy.ndarray): The second image to perform arithmetic operations with.
            alpha (float): The alpha value for the operation.
            operation (str): The arithmetic operation to be performed. Options are "Add", "Subtract", "Multiply", "Divide".
        Returns:
            imageBGRA (numpy.ndarray): The resulting image after the arithmetic operation in the BGRA format.
        """
        imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR).astype(np.float32)  # convert the BGRA image to BGR color space
        
        # resize the second image to match the size of the first image and multiply with alpha
        secondImage = cv2.resize(secondImage, (imageBGRA.shape[1], imageBGRA.shape[0])).astype(np.float32) * alpha  
        
        # perform the selected arithmetic operation    
        if operation == "Add":
            imageBGR = cv2.add(imageBGR, secondImage)
        elif operation == "Subtract":
            imageBGR = cv2.subtract(imageBGR, secondImage)
        elif operation == "Multiply":
            imageBGR = cv2.multiply(imageBGR, secondImage)
        elif operation == "Divide":
            imageBGR = cv2.divide(imageBGR, secondImage + 1e-10)

        imageBGR = np.clip(imageBGR, 0, 255).astype(np.uint8)       # clip the values to the range [0, 255]
        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       # set back the alpha channel to make it BGRA

        return imageBGRA
    

    def perform_image_logic(self, imageBGRA, secondImage, operation):
        """
        Performs logical operations on the given image and a second image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            secondImage (numpy.ndarray): The second image to perform logical operations with.
            operation (str): The logical operation to be performed. Options are "And", "Or", "Xor".
        Returns:
            imageBGRA (numpy.ndarray): The resulting image after the logical operation in the BGRA format.
        """
        imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)              # convert the BGRA image to BGR color space
        
        # resize the second image to match the size of the first image
        secondImage = cv2.resize(secondImage, (imageBGRA.shape[1], imageBGRA.shape[0]))  
        
        # perform the selected arithmetic operation    
        if operation == "And":
            imageBGR = cv2.bitwise_and(imageBGR, secondImage)
        elif operation == "Or":
            imageBGR = cv2.bitwise_or(imageBGR, secondImage)
        elif operation == "Xor":
            imageBGR = cv2.bitwise_xor(imageBGR, secondImage)

        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))               # set back the alpha channel to make it BGRA

        return imageBGRA
        

    def get_laplacian_filter(self, imageBGRA, extended=False, normalize=False):
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

        imageHSVA = self.bgra2hsva_transform(imageBGRA)                                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2].astype(np.float32) / 255.0                    # get the V channel of the HSVA image
        laplace = cv2.filter2D(vChannel, -1, w, borderType=cv2.BORDER_REPLICATE)    # apply the laplace filter to the V channel

        # normalize the filtered image if the normalize switch is checked
        if normalize:
            laplace = cv2.normalize(laplace, None, 0, 1, cv2.NORM_MINMAX)
        
        laplace = (np.clip(laplace, 0, 1) * 255).astype(np.uint8)                   # clip the values to the range [0, 255]  
        imageBGR = cv2.cvtColor(laplace, cv2.COLOR_GRAY2BGR)                        # mkae the laplace image 3 channel
        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))                       # set back the alpha channel to make it BGRA
        
        return imageBGRA
    

    def get_sobel_filter(self, imageBGRA, normalize=False):
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

        imageHSVA = self.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2].astype(np.float32) / 255.0    # get the V channel of the HSVA image

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


    def apply_order_stat_filter(self, imageBGRA, kernelSize, order, mask=None):
        """
        Applies order statistics filter to the V channel of the given image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            kernelSize (int): The size of the kernel for the filter.
            order (str): The order statistic to be applied. Options are "max", "min", "median".
            mask (numpy.ndarray): A mask to apply the filter only to certain pixels.
        Returns:
            imageBGRA (numpy.ndarray): The image with order statistics filter applied in the BGRA format.
        """
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image

        # apply the order statistics filter to the V channel
        if order == "max":
            vChannel = cv2.dilate(vChannel, np.ones((kernelSize, kernelSize), np.uint8), borderType=cv2.BORDER_REPLICATE)   
        elif order == "min":
            vChannel = cv2.erode(vChannel, np.ones((kernelSize, kernelSize), np.uint8),borderType=cv2.BORDER_REPLICATE)     
        elif order == "median":
            vChannel = cv2.medianBlur(vChannel, kernelSize)  

        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSVA[:, :, 2] = vChannel if mask is None else np.where(mask > 0, vChannel, imageHSVA[:, :, 2])

        imageBGRA = self.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA
    

    def apply_box_filter(self, imageBGRA, kernelSize, mask=None):
        """
        Applies box filter to the V channel of the given image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            kernelSize (int): The size of the kernel for the filter.
            mask (numpy.ndarray): A mask to apply the box filter only to certain pixels.
        Returns:
            imageBGRA (numpy.ndarray): The image with box filter applied in the BGRA format.
        """
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image

        # apply the box filter to the V channel
        vChannel = cv2.blur(vChannel, (kernelSize, kernelSize), borderType=cv2.BORDER_REPLICATE)    

        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSVA[:, :, 2] = vChannel if mask is None else np.where(mask > 0, vChannel, imageHSVA[:, :, 2])

        imageBGRA = self.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA
    

    def apply_gaussian_blur(self, imageBGRA, kernelSize, sigma, mask=None):
        """
        Applies Gaussian blur to the V channel of the given image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            kernelSize (int): The size of the kernel for the filter.
            sigma (float): The standard deviation for the Gaussian kernel.
            mask (numpy.ndarray): A mask to apply the Gaussian blur only to certain pixels.
        Returns:
            imageBGRA (numpy.ndarray): The image with Gaussian blur applied in the BGRA format.
        """
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image

        # apply the gaussian blur to the V channel
        vChannel = cv2.GaussianBlur(vChannel, (kernelSize, kernelSize), sigma, borderType=cv2.BORDER_REPLICATE)  
        
        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSVA[:, :, 2] = vChannel if mask is None else np.where(mask > 0, vChannel, imageHSVA[:, :, 2])

        imageBGRA = self.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA


    def apply_laplacian_sharpening(self, imageBGRA, alpha, extended=False, mask=None):
        """
        Applies Laplacian sharpening to the V channel of the given image.   
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            alpha (float): The scaling factor for the V channel of the image.
            extended (bool): If True, use extended Laplacian kernel. Default is False.
            mask (numpy.ndarray): A mask to apply the Laplacian sharpening only to certain pixels.
        Returns:
            imageBGRA (numpy.ndarray): The image with Laplacian sharpening applied in the BGRA format.
        """
        # create the laplace kernel
        if extended:
            w = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
        else:
            w = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)

        imageHSVA = self.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image
        vChannel = vChannel.astype(np.float32) / 255.0              # normalize the image to 0-1 range
        
        laplace = cv2.filter2D(vChannel, cv2.CV_32F, w, borderType=cv2.BORDER_REPLICATE)   # get the laplacian filter
        vChannel = vChannel - laplace * alpha                       # sharpen the image using the laplacian filter
        vChannel = np.clip(vChannel, 0, 1)                          # clip the image to 0-1 range
        vChannel = (vChannel * 255).astype(np.uint8)                # convert back to uint8

        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSVA[:, :, 2] = vChannel if mask is None else np.where(mask > 0, vChannel, imageHSVA[:, :, 2])

        imageBGRA = self.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA
    

    def apply_sobel_sharpening(self, imageBGRA, alpha, mask=None):
        """
        Applies Sobel sharpening to the V channel of the given image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            alpha (float): The scaling factor for the V channel of the image.
            mask (numpy.ndarray): A mask to apply the Sobel sharpening only to certain pixels.
        Returns:
            imageBGRA (numpy.ndarray): The image with Sobel sharpening applied in the BGRA format.
        """
        # create the sobel kernels
        w_x = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
        w_y = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)

        imageHSVA = self.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image
        vChannel = vChannel.astype(np.float32) / 255.0              # normalize the image to 0-1 range

        # apply sobel kernel on x axis
        laplace_x = cv2.filter2D(vChannel, cv2.CV_32F, w_x, borderType=cv2.BORDER_REPLICATE)  
        vChannel = vChannel + laplace_x * alpha                     # sharpen the image using the sobel filter

        # apply sobel kernel on y axis
        laplace_y = cv2.filter2D(vChannel, cv2.CV_32F, w_y, borderType=cv2.BORDER_REPLICATE)  
        vChannel = vChannel + laplace_y * alpha                     # sharpen the image using the sobel filter
        vChannel = np.clip(vChannel, 0, 1)                          # clip the image to 0-1 range
        vChannel = (vChannel * 255).astype(np.uint8)                # convert back to uint8

        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSVA[:, :, 2] = vChannel if mask is None else np.where(mask > 0, vChannel, imageHSVA[:, :, 2])

        imageBGRA = self.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA


    def apply_unsharp_mask(self, imageBGRA, kernelSize, sigma, alpha, mask=None):
        """
        Applies unsharp masking to the V channel of the given image.
        Args:
            imageBGRA (numpy.ndarray): The input image in the BGRA format.
            kernelSize (int): The size of the kernel for the filter.
            sigma (float): The standard deviation for the Gaussian kernel.
            alpha (float): The scaling factor for the V channel of the image.
            mask (numpy.ndarray): A mask to apply the unsharp masking only to certain pixels.
        Returns:
            imageBGRA (numpy.ndarray): The image with unsharp masking applied in the BGRA format.
        """
        imageHSVA = self.bgra2hsva_transform(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image
        vChannel = vChannel.astype(np.float32) / 255.0              # normalize the image to 0-1 range

        Blurred = cv2.GaussianBlur(vChannel, (kernelSize, kernelSize), sigma, borderType=cv2.BORDER_REPLICATE)     
        Sharp = vChannel - Blurred                                  # get the sharpened filter
        vChannel = vChannel + Sharp * alpha                         # sharpen the image
        vChannel = np.clip(vChannel, 0, 1)                          # clip the image to 0-1 range
        vChannel = (vChannel * 255).astype(np.uint8)                # convert back to uint8

        # If a mask is provided, use it to update only the pixels where mask != 0
        imageHSVA[:, :, 2] = vChannel if mask is None else np.where(mask > 0, vChannel, imageHSVA[:, :, 2])

        imageBGRA = self.hsva2bgra_transform(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA
    

