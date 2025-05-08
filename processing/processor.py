import numpy as np
import cv2


class Processor():
    """
    """
    def __init__(self):
        pass


    def bgra2hsva(self, imageBGRA):
        """
        Converts the given image from BGRA to HSVA color space.
        This method is used to convert the image to a format suitable for processing.
        """
        imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)        # convert the BGR image to HSV color space
        imageHSVA = cv2.merge((imageHSV, imageBGRA[:, :, 3]))                  # set the alpha channel of the image
        return imageHSVA
    

    def hsva2bgra(self, imageHSVA):
        """
        Converts the given image from HSVA to BGRA color space.
        This method is used to convert the image back to its original format after processing.
        """
        imageBGR = cv2.cvtColor(imageHSVA[:, :, :3], cv2.COLOR_HSV2BGR)         # convert the HSVA image to BGR color space
        imageBGRA = cv2.merge((imageBGR, imageHSVA[:, :, 3]))                  # set the alpha channel of the image
        return imageBGRA
    

    def isGrayscale(self, imageBGRA):
        """
        Checks if the given image is grayscale.
        This method is used to determine if the image has color information or not.
        """
        return (np.array_equal(imageBGRA[:, :, 0], imageBGRA[:, :, 1]) and np.array_equal(imageBGRA[:, :, 1], imageBGRA[:, :, 2]))


    def brightness(self, imageBGRA, value):
        """
        """
        imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space
        imageHSVA[:, :, 2] = cv2.add(imageHSVA[:, :, 2], value)     # brighten the V channel of the HSVA image
        imageBGRA = self.hsva2bgra(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA


    def saturation(self, imageBGRA, value):
        """
        """
        if not self.isGrayscale(imageBGRA):
            imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space
            imageHSVA[:, :, 1] = cv2.add(imageHSVA[:, :, 1], value)     # brighten the V channel of the HSVA image
            imageBGRA = self.hsva2bgra(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA
    

    def contrastByRange(self, imageBGRA, inRange, outRange):
        """
        """
        imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space
        
        # calculate the alpha and beta values
        alpha = (outRange[1] - outRange[0]) / (inRange[1] - inRange[0])
        beta = outRange[0] - (alpha * inRange[0])
        imageHSVA[:, :, 2] = cv2.convertScaleAbs(imageHSVA[:, :, 2], -1, alpha, beta) 

        imageBGRA = self.hsva2bgra(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA


    def contrastByT(self, imageBGRA, alpha, beta):
        """
        """
        imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space

        # apply the contrast adjustment to the v channel of the HSVA image
        imageHSVA[:, :, 2] = cv2.convertScaleAbs(imageHSVA[:, :, 2], -1, alpha, beta) 

        imageBGRA = self.hsva2bgra(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA


    def fullScaleContrast(self, imageBGRA):
        """
        """
        imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space

        # perform full scale contrast stretching
        imageHSVA[:, :, 2] = cv2.normalize(imageHSVA[:, :, 2], None, 0, 255, cv2.NORM_MINMAX)

        imageBGRA = self.hsva2bgra(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA


    def logTransform(self, imageBGRA):
        """
        """        
        imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image
        vChannel = vChannel.astype(np.float32)                      # convert the v channel to float32 for log transformation
        vChannel = np.log(1 + vChannel)                             # apply log transformation
        vChannel = cv2.normalize(vChannel, None, 0, 255, cv2.NORM_MINMAX)
        imageHSVA[:, :, 2] = vChannel.astype(np.uint8)              # update the V channel of the HSVA image
        imageBGRA = self.hsva2bgra(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA


    def gammaTransform(self, imageBGRA, gamma):
        """
        """
        imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image
        vChannel = vChannel.astype(np.float32)/255                  # convert the v channel to float32 for gamma transformation
        vChannel = cv2.pow(vChannel, gamma)                         # apply gamma transformation
        imageHSVA[:, :, 2] = (vChannel*255).astype(np.uint8)        # update the V channel of the HSVA image
        imageBGRA = self.hsva2bgra(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA
    

    def rgb2gray(self, imageBGRA):
        """
        """
        imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space
        gray = imageHSVA[:, :, 2]                                   # get only the V channel of the HSVA image
        grayBGR = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)            # make the binary image 3 channel
        grayBGRA = cv2.merge((grayBGR, imageBGRA[:, :, 3]))         # set back the alpha channel of the image

        return grayBGRA
    

    def threshold(self, imageBGRA, threshold):
        """
        """
        imageHSVA = self.bgra2hsva(imageBGRA)                               # convert the image to HSVA color space
        gray = imageHSVA[:, :, 2]                                           # get only the V channel of the HSVA image
        imageBW = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1] # convert v channel to binary
        BW_BGR = cv2.cvtColor(imageBW, cv2.COLOR_GRAY2BGR)                  # make the binary image 3 channel
        BW_BGRA = cv2.merge((BW_BGR, imageBGRA[:, :, 3]))                   # set back the alpha channel of the image

        return BW_BGRA


    def complement(self, imageBGRA):
        """
        """
        imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)          
        imageBGR = cv2.bitwise_not(imageBGR)                         
        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       
        return imageBGRA


    def crop(self, imageBGRA, leftCut, rightCut, topCut, bottomCut):
        """
        """
        h, w = imageBGRA.shape[:2]            # get the height and width of the image

        # if the crop values are valid, crop the image
        if leftCut+rightCut < w or topCut+bottomCut < h:
            imageBGRA =  imageBGRA[topCut:-1-bottomCut, leftCut:-1-rightCut]  

        return imageBGRA

   
    def flip(self, imageBGRA, flipCode):
        """
        """
        imageBGRA = cv2.flip(imageBGRA, flipCode)       # flip the image based on the provided flip code

        return imageBGRA


    def rotate(self, imageBGRA, angle):
        """
        """
        (h, w) = imageBGRA.shape[:2]            # get the height and width of the image
        center = (w // 2, h // 2)           # rotate the center of the image
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        imageBGRA = cv2.warpAffine(imageBGRA, M, (w, h))

        return imageBGRA


    def resize(self, imageBGRA, newWidth, newHeight):
        """
        """
        imageBGRA = cv2.resize(imageBGRA, (newWidth, newHeight))       # resize the image to the specified size

        return imageBGRA


    def padding(self, imageBGRA, paddingType, leftPad, rightPad, topPad, bottomPad, constant):
        """
        """
        imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)          # convert the BGRA image to BGR color space

        # apply padding to the image
        if paddingType == cv2.BORDER_CONSTANT:
            imageBGR = cv2.copyMakeBorder(imageBGR, topPad, bottomPad, leftPad, rightPad, paddingType, value=(constant, constant, constant))
            imageA = cv2.copyMakeBorder(imageBGRA[:, :, 3], topPad, bottomPad, leftPad, rightPad, cv2.BORDER_CONSTANT, value=255)
        else:
            imageBGR = cv2.copyMakeBorder(imageBGR, topPad, bottomPad, leftPad, rightPad, paddingType)
            imageA = cv2.copyMakeBorder(imageBGRA[:, :, 3], topPad, bottomPad, leftPad, rightPad, cv2.BORDER_CONSTANT, value=255)

        imageBGRA = cv2.merge((imageBGR, imageA))       # set back the alpha channel of the image

        return imageBGRA
    

    def histogramEqualization(self, imageBGRA):
        """
        """
        imageHSVA = self.bgra2hsva(imageBGRA)                           # convert the image to HSVA color space
        imageHSVA[:, :, 2] = cv2.equalizeHist(imageHSVA[:, :, 2])       # equalize the V channel of the HSVA image
        imageBGRA = self.hsva2bgra(imageHSVA)                           # convert back to BGRA color space
        return imageBGRA


    def clahe(self, imageBGRA, clipLimit, tileGridSize):
        """
        """
        imageHSVA = self.bgra2hsva(imageBGRA)                           # convert the image to HSVA color space
        clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(tileGridSize, tileGridSize))
        imageHSVA[:, :, 2] = clahe.apply(imageHSVA[:, :, 2])            # apply CLAHE to the V channel of the HSVA image
        imageBGRA = self.hsva2bgra(imageHSVA)                           # convert back to BGRA color space
        return imageBGRA
    

    def masking(self, imageBGRA, lowerBound, upperBound):
        """
        """
        imageHSVA = self.bgra2hsva(imageBGRA)                           # convert the image to HSVA color space
        mask = cv2.inRange(imageHSVA[:, :, :3], lowerBound, upperBound) # create a mask based on the range values
        imageBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)               # convert the mask to grayscale
        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))           # set back the alpha channel of the image

        return imageBGRA


    def bitSlice(self, imageBGRA, bitPlane):
        """
        """
        imageHSVA = self.bgra2hsva(imageBGRA)                           # convert the image to HSVA color space
        imageGray = cv2.bitwise_and(imageHSVA[:, :, 2], 1 << bitPlane)         # get the selected bit plane
        imageBinary = np.where(imageGray > 0, 255, 0).astype(np.uint8)    # convert the bit plane to binary image
        imageBGR = cv2.cvtColor(imageBinary, cv2.COLOR_GRAY2BGR)          # make the binary image 3 channel
        imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)              # convert back to HSV color space
        imageHSVA = cv2.merge((imageHSV, imageBGRA[:, :, 3]))             # set back the alpha channel of the image
        imageBGRA = self.hsva2bgra(imageHSVA)                           # convert back to BGRA color space
        return imageBGRA
    

    def gaussianNoise(self, imageBGRA, mean, std):
        """
        """
        imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)          # convert the BGRA image to BGR color space

        # If the image is grayscale, make the noise channels identical
        if self.isGrayscale(imageBGRA):
            noise = np.random.normal(mean, std, imageBGR[:, :, 0].shape).astype(np.float32) 
            noise = cv2.merge((noise, noise, noise))
        else:
            noise = np.random.normal(mean, std, imageBGR.shape).astype(np.float32)

        imageBGR = imageBGR.astype(np.float32) + noise              # add noise
        imageBGR = np.clip(imageBGR, 0, 255).astype(np.uint8)       # clip the values to the range [0, 255]
        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       # set back the alpha channel of the image
        
        return imageBGRA


    def saltPepperNoise(self, imageBGRA, saltPepProb):
        """
        """
        imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)          # convert the BGRA image to BGR color space

        numSalt = int(imageBGR.size * saltPepProb)       # number of salt pixels to add
        numPep = int(imageBGR.size * saltPepProb)         # number of pepper pixels to add

        saltCoords = [np.random.randint(0, i-1, numSalt) for i in imageBGR.shape]
        pepCoords = [np.random.randint(0, i-1, numPep) for i in imageBGR.shape]
        
        imageBGR[saltCoords[0], saltCoords[1]] = [255, 255, 255]    # add salt noise
        imageBGR[pepCoords[0], pepCoords[1]] = [0,0,0]              # add pepper noise

        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       # set back the alpha channel of the image
        
        return imageBGRA    


    def poissonNoise(self, imageBGRA):
        """
        """
        imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)
        if self.isGrayscale(imageBGRA):
            imageGray = np.random.poisson(imageBGR[:, :, 0].astype(np.float32))
            imageBGR = cv2.merge((imageGray, imageGray, imageGray))
        else:
            imageBGR = np.random.poisson(imageBGR.astype(np.float32))
        
        
        imageBGR = np.clip(imageBGR, 0, 255).astype(np.uint8)       
        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       # set back the alpha channel of the image

        return imageBGRA


    def arithmetic(self, imageBGRA, secondImage, alpha, operation):
        """
        """
        secondImage = (secondImage * alpha).astype(np.float32)  # multiply the second image with alpha value
        secondImage = cv2.resize(secondImage, (imageBGRA.shape[1], imageBGRA.shape[0]))  # resize the second image to match the size of the first image
        imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR).astype(np.float32)  # convert the BGRA image to BGR color space
        
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
        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       # set back the alpha channel of the image

        return imageBGRA
    

    def logic(self, imageBGRA, secondImage, operation):
        """
        """
        secondImage = cv2.resize(secondImage, (imageBGRA.shape[1], imageBGRA.shape[0]))  # resize the second image to match the size of the first image
        imageBGR = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)                           # convert the BGRA image to BGR color space
        
        # perform the selected arithmetic operation    
        if operation == "And":
            imageBGR = cv2.bitwise_and(imageBGR, secondImage)
        elif operation == "Or":
            imageBGR = cv2.bitwise_or(imageBGR, secondImage)
        elif operation == "Xor":
            imageBGR = cv2.bitwise_xor(imageBGR, secondImage)

        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       # set back the alpha channel of the image

        return imageBGRA
        

    def laplacian(self, imageBGRA, extended=False, normalize=False):
        """
        """
        # create the laplace kernel
        if extended:
            w = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
        else:
            w = np.array([[0, 1, 0], [0, -4, 0], [0, 1, 0]], dtype=np.float32)

        imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image
        vChannel = vChannel.astype(np.float32) / 255.0


        laplace = cv2.filter2D(vChannel, -1, w, borderType=cv2.BORDER_REPLICATE)

        # normalize the filtered image if the normalize switch is checked
        if normalize:
            laplace = cv2.normalize(laplace, None, 0, 1, cv2.NORM_MINMAX)
        
        laplace = (np.clip(laplace, 0, 1) * 255).astype(np.uint8)
        imageBGR = cv2.merge((laplace, laplace, laplace))  
        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       # set back the alpha channel of the image
        
        return imageBGRA
    

    def sobel(self, imageBGRA, normalize=False):
        """
        """
        # create the sobel kernels
        w_x = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
        w_y = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)

        imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image
        vChannel = vChannel.astype(np.float32) / 255.0

        # get the sobel filters
        sobel_x = cv2.filter2D(vChannel, -1, w_x, borderType=cv2.BORDER_REPLICATE)
        sobel_y = cv2.filter2D(vChannel, -1, w_y, borderType=cv2.BORDER_REPLICATE)
        sobel = np.sqrt(sobel_x ** 2 + sobel_y ** 2)

        # normalize the filtered image if the normalize switch is checked
        if normalize:
            sobel = cv2.normalize(sobel, None, 0, 1, cv2.NORM_MINMAX)

        sobel = (np.clip(sobel, 0, 1) * 255).astype(np.uint8)
        imageBGR = cv2.merge((sobel, sobel, sobel))
        imageBGRA = cv2.merge((imageBGR, imageBGRA[:, :, 3]))       # set back the alpha channel of the image
        
        return imageBGRA


    def orderStatistics(self, imageBGRA, kernelSize, order):
        """
        """
        imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image

        if order == "max":
            vChannel = cv2.dilate(vChannel, np.ones((kernelSize, kernelSize), np.uint8), borderType=cv2.BORDER_REPLICATE)   
        elif order == "min":
            vChannel = cv2.erode(vChannel, np.ones((kernelSize, kernelSize), np.uint8),borderType=cv2.BORDER_REPLICATE)     
        elif order == "median":
            vChannel = cv2.medianBlur(vChannel, kernelSize)  

        imageHSVA[:, :, 2] = vChannel                               # update the V channel of the HSVA image
        imageBGRA = self.hsva2bgra(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA
    

    def boxFilter(self, imageBGRA, kernelSize):
        """
        """
        imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image

        vChannel = cv2.blur(vChannel, (kernelSize, kernelSize), borderType=cv2.BORDER_REPLICATE)    

        imageHSVA[:, :, 2] = vChannel                               # update the V channel of the HSVA image
        imageBGRA = self.hsva2bgra(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA
    

    def gaussianBlur(self, imageBGRA, kernelSize, sigma):
        """
        """
        imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image

        vChannel = cv2.GaussianBlur(vChannel, (kernelSize, kernelSize), sigma, borderType=cv2.BORDER_REPLICATE)  
        
        imageHSVA[:, :, 2] = vChannel                               # update the V channel of the HSVA image
        imageBGRA = self.hsva2bgra(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA


    def laplacianSharpening(self, imageBGRA, alpha, extended=False):
        """
        """
        # create the laplace kernel
        if extended:
            w = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
        else:
            w = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)

        imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image
        vChannel = vChannel.astype(np.float32) / 255                # normalize the image to 0-1 range
        
        laplace = cv2.filter2D(vChannel, cv2.CV_32F, w, borderType=cv2.BORDER_REPLICATE)   # get the laplacian filter
        vChannel = vChannel - laplace * alpha                       # sharpen the image using the laplacian filter

        vChannel = np.clip(vChannel, 0, 1)                          # clip the image to 0-1 range
        vChannel = (vChannel * 255).astype(np.uint8)                # convert back to uint8

        imageHSVA[:, :, 2] = vChannel                               # update the V channel of the HSVA image
        imageBGRA = self.hsva2bgra(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA
    

    def sobelSharpening(self, imageBGRA, alpha):
        """
        """
        # create the sobel kernels
        w_x = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
        w_y = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)

        imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image
        vChannel = vChannel.astype(np.float32) / 255                # normalize the image to 0-1 range

        # apply sobel kernel on x axis
        laplace_x = cv2.filter2D(vChannel, cv2.CV_32F, w_x, borderType=cv2.BORDER_REPLICATE)  
        vChannel = vChannel + laplace_x * alpha                     # sharpen the image using the sobel filter

        # apply sobel kernel on y axis
        laplace_y = cv2.filter2D(vChannel, cv2.CV_32F, w_y, borderType=cv2.BORDER_REPLICATE)  
        vChannel = vChannel + laplace_y * alpha                     # sharpen the image using the sobel filter

        vChannel = np.clip(vChannel, 0, 1)                          # clip the image to 0-1 range
        vChannel = (vChannel * 255).astype(np.uint8)                # convert back to uint8

        imageHSVA[:, :, 2] = vChannel                               # update the V channel of the HSVA image
        imageBGRA = self.hsva2bgra(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA


    def unsharpMasking(self, imageBGRA, kernelSize, sigma, alpha):
        """
        """
        imageHSVA = self.bgra2hsva(imageBGRA)                       # convert the image to HSVA color space
        vChannel = imageHSVA[:, :, 2]                               # get the V channel of the HSVA image
        vChannel = vChannel.astype(np.float32) / 255                # normalize the image to 0-1 range


        Blurred = cv2.GaussianBlur(vChannel, (kernelSize, kernelSize), sigma, borderType=cv2.BORDER_REPLICATE)     
        Sharp = vChannel - Blurred                                  # get the sharpened filter
        vChannel = vChannel + Sharp * alpha                         # sharpen the image

        vChannel = np.clip(vChannel, 0, 1)                          # clip the image to 0-1 range
        vChannel = (vChannel * 255).astype(np.uint8)                # convert back to uint8

        imageHSVA[:, :, 2] = vChannel                               # update the V channel of the HSVA image
        imageBGRA = self.hsva2bgra(imageHSVA)                       # convert back to BGRA color space

        return imageBGRA