import numpy as np
import cv2

from PySide6.QtCore import Qt, Signal, QMimeData
from PySide6.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, 
                               QSizePolicy, QFrame, QCheckBox, QComboBox, QFileDialog)
from PySide6.QtGui import QFont, QDrag

from processing.processor import Processor
import constants
import utils
from ui.components import UiComponents 


class AddNewBox(QWidget):
    """
    A box that allows the user to add a new function.
    """
    # Signal to communicate with the main application
    trigger = Signal(str)

    def __init__(self):
        super().__init__()

        # make the widget fixed size
        self.setFixedWidth(200)
        
        # set a font size variable
        self.font = QFont()              
        self.font.setPointSize(10)  

        # set the layout for the widget
        mainLayout = QVBoxLayout(self) 
        mainLayout.setContentsMargins(0, 0, 0, 0)

        # create a frame to hold the content
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("QFrame#Frame { border: 2px solid gray; border-radius: 10px; }")
        frame.setObjectName("Frame")
        frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        frame.setFixedWidth(200)
        mainLayout.addWidget(frame)     

        # create a layout inside the frame
        self.frameLayout = QVBoxLayout(frame)
        self.frameLayout.setContentsMargins(10, 10, 10, 10)

        # create a title label
        label = QLabel("Add New")
        label.setFont(self.font)
        label.setAlignment(Qt.AlignHCenter)
        self.frameLayout.addWidget(label)
        
        # Create a combo box to select the function type
        self.combo = QComboBox()
        self.combo.addItems(constants.function_names)
        self.combo.setFont(self.font)
        self.combo.setStyleSheet("padding: 5px;")  
        self.frameLayout.addWidget(self.combo, alignment=Qt.AlignVCenter)

        view = self.combo.view()
        view.setMouseTracking(False)  
        view.setAutoScroll(False)     
    
        # Create a button to add a new function
        newBtn = QPushButton("+")
        font = QFont()              
        font.setPointSize(20)  
        newBtn.setFont(font) 
        newBtn.setStyleSheet("padding-top: 5px; padding-bottom: 10px;")     
        newBtn.clicked.connect(lambda: self.trigger.emit(self.combo.currentText()))  
        self.frameLayout.addWidget(newBtn, alignment=Qt.AlignVCenter)



class FunctionBox(QWidget):
    """
    A base class for creating function boxes in the GUI.
    This class provides a template for creating specific function boxes by subclassing it.
    """
    # Signals to communicate with the main application
    updateTrigger = Signal()
    removeTrigger = Signal(str)
   

    def __init__(self, title="Function", parent=None):
        super().__init__(parent)

        self.contentLayout = QVBoxLayout()
        self.processor = Processor()        # create an instance of the Processor class
        # create an instance of the self.ui_components class
        self.ui_components = UiComponents(parent_widget=self.contentLayout, onchange_trigger=self.updateTrigger)        
        self.initiate_ui(title)             # call the initiate_ui method to set up the UI


    def initiate_ui(self, title):
        """
        """
        self.title = title                  # set the title of the function box
        self.setFixedWidth(200)             # make the widget fixed size
        
        # set a font size variable
        self.font = QFont()              
        self.font.setPointSize(10)  

        # set the layout for the widget
        mainLayout = QVBoxLayout(self) 
        mainLayout.setContentsMargins(0, 0, 0, 0)

        # create a frame to hold the content
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("QFrame#Frame { border: 2px solid gray; border-radius: 10px; }")
        frame.setObjectName("Frame")
        frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        frame.setFixedWidth(200)
        mainLayout.addWidget(frame)     

        # create a layout inside the frame
        frameLayout = QVBoxLayout(frame)
        frameLayout.setContentsMargins(10, 10, 10, 10)

        # create a horizontal layout for the title and remove button
        titleLayout = QHBoxLayout()
        frameLayout.addLayout(titleLayout, 1)
        titleLayout.setAlignment(Qt.AlignTop)

        # create a title label
        label = QLabel(title)
        label.setFont(self.font)
        titleLayout.addWidget(label)

        # create a button to remove the function box
        removeBtn = QPushButton("X")
        removeBtn.setFont(self.font)
        removeBtn.setFixedWidth(30)
        removeBtn.clicked.connect(lambda: self.removeTrigger.emit(title))
        titleLayout.addWidget(removeBtn,1)
        
        # create a layout for the ON/OFF switch
        switchLayout = QHBoxLayout()
        frameLayout.addLayout(switchLayout, 1)

        # create ON/OFF switch
        self.switch = QCheckBox("On/Off")
        self.switch.setChecked(True)
        self.switch.setFont(self.font)
        self.switch.stateChanged.connect(lambda: self.updateTrigger.emit())
        self.switch.setFixedHeight(30)
        switchLayout.addWidget(self.switch, alignment=Qt.AlignTop)

        # add the content layout to the frame layout
        frameLayout.addLayout(self.contentLayout, 4)

        # add a dummy widget to fill the space
        dummy = QWidget()
        dummy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.contentLayout.addWidget(dummy)
    


class DraggableFunctionBox(FunctionBox):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragStartPosition = event.position()

    def mouseMoveEvent(self, event):
        if not event.buttons() & Qt.LeftButton:
            return
        if (event.position() - self.dragStartPosition).manhattanLength() < 10:
            return

        drag = QDrag(self)
        mimeData = QMimeData()
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.position().toPoint())
        drag.setPixmap(self.grab())
        drag.exec(Qt.MoveAction)



class BrightnessBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(constants.BRIGHTNESS_NAME, parent)

        # Create a slider to adjust brightness
        self.brightness = self.ui_components.slider(heading="Brightness", minValue=-50, maxValue=50)  

    def execute(self, imageBGRA):
        imageBGRA = self.processor.brightness(imageBGRA, self.brightness[0].value())  

        return imageBGRA


class SaturationBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(constants.SATURATION_NAME, parent)

        # Create a slider to adjust saturation
        self.saturation = self.ui_components.slider(heading="Saturation", minValue=-50, maxValue=50)

    def execute(self, imageBGRA):
        imageBGRA = self.processor.saturation(imageBGRA, self.saturation[0].value())     

        return imageBGRA


class ContrastBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(constants.CONTRAST_NAME, parent)

        self.slider_rescale = 10

        # create a combo list to select between input type (range or T(s))
        self.combo = self.ui_components.combo_list(["by Input-Output Range", "by T(s)"])

        # Create min and max input boxes for input range
        self.inMinMax = self.ui_components.dual_input("Input Range:")
        # Create min and max input boxes for output range
        self.outMinMax = self.ui_components.dual_input("Output Range:")

        # Create sliders for alpha and beta values
        self.alpha = self.ui_components.slider(heading="Alpha:", minValue=1, maxValue=30, defaultValue=10, rescale=self.slider_rescale)
        self.beta = self.ui_components.slider(heading="Beta:", minValue=-50, maxValue=50)  

        # connect the combo box to the on_change function
        self.ui_components.set_combo_adapt_widgets(self.combo, [[self.inMinMax, self.outMinMax], [self.alpha, self.beta]])

    def execute(self, imageBGRA):

        if self.combo.currentText() == "by Input-Output Range":
            # get input and output range values from the text boxes
            in_min, in_max = self.ui_components.get_component_value(self.inMinMax[:2], maxs=[255,255], defaults=[0, 255])
            out_min, out_max = self.ui_components.get_component_value(self.outMinMax[:2], maxs=[255,255], defaults=[0, 255])

            # apply contrast stretching using input-output range method
            imageBGRA = self.processor.contrastByRange(imageBGRA, [in_min, in_max], [out_min, out_max])  

            return imageBGRA  

        elif self.combo.currentText() == "by T(s)":
            # get the alpha and beta values from sliders
            alpha = self.alpha[0].value() / self.slider_rescale
            beta = self.beta[0].value()

            # apply contrast stretching using T(s) method
            imageBGRA = self.processor.contrastByT(imageBGRA, alpha, beta)  
            
            return imageBGRA
              

class FullScaleContrastBox(DraggableFunctionBox):
    """
    A box that performs full scale contrast stretching on the image.
    """
    def __init__(self, parent=None):
        super().__init__(constants.FULL_SCALE_CONTRAST_NAME, parent)
  

    def execute(self, imageBGRA):
        # apply full scale contrast stretching
        imageBGRA = self.processor.fullScaleContrast(imageBGRA)  
        
        return imageBGRA


class LogBox(DraggableFunctionBox):
    """
    A box that performs log transformation on the image.
    """
    def __init__(self, parent=None):
        super().__init__(constants.LOG_NAME, parent)
  

    def execute(self, imageBGRA):
        # apply log transformation
        imageBGRA = self.processor.logTransform(imageBGRA)  

        return imageBGRA


class GammaBox(DraggableFunctionBox):
    """
    A box that performs gamma transformation on the image.
    This is a non-linear transformation that can be used to adjust the brightness and contrast of the image.
    """
    def __init__(self, parent=None):
        super().__init__(constants.GAMMA_NAME, parent)

        self.slider_rescale = 10

        # insert signle input box for gamma value
        self.gamma = self.ui_components.slider(heading="Gamma:", minValue=1, maxValue=100, defaultValue=10, rescale=self.slider_rescale)

    def execute(self, imageBGRA):
        # get the threshold value from slider
        gamma = self.gamma[0].value() / self.slider_rescale
        
        # apply gamma transformation
        imageBGRA = self.processor.gammaTransform(imageBGRA, gamma)  

        return np.uint8(imageBGRA)     


class RGB2GrayBox(DraggableFunctionBox):
    """
    A box that converts image from RGB to grayscale.
    This class provides a UI for specifying the conversion and processes the image accordingly.
    """
    def __init__(self, parent=None):
        super().__init__(constants.RGB2GRAY_NAME, parent)

    def execute(self, imageBGRA):
        # apply RGB to grayscale conversion
        imageBGRA = self.processor.rgb2gray(imageBGRA)              

        return imageBGRA


class ThresholdingBox(DraggableFunctionBox):
    """
    A box that converts image to black and white by thresholding.
    """
    def __init__(self, parent=None):
        super().__init__(constants.THRESHOLDING_NAME, parent)

        # insert slider for threshold value
        self.threshold = self.ui_components.slider(heading="Threshold:", minValue=0, maxValue=255, defaultValue=128)

    def execute(self, imageBGRA):
        # get the threshold value from slider
        threshold = self.threshold[0].value()                                       

        # apply thresholding
        imageBGRA = self.processor.threshold(imageBGRA, threshold)          
        
        return imageBGRA


class ComplementBox(DraggableFunctionBox):
    """
    A box that performs complememnt of image.
    This is a simple image processing operation that inverts the colors of the image.
    """
    def __init__(self, parent=None):
        super().__init__(constants.COMPLEMENT_NAME, parent)
  
    def execute(self, imageBGRA):
        # apply complement operation
        imageBGRA = self.processor.complement(imageBGRA)  

        return imageBGRA


class CropBox(DraggableFunctionBox):
    """
    A box that allows the user to crop the image.
    This class provides a UI for specifying the crop ranges and processes the image accordingly.
    """
    def __init__(self, parent=None):
        super().__init__(constants.CROP_NAME, parent)

        # Create input boxes for crop ranges
        self.leftRight  = self.ui_components.dual_input("Left-Right:", 0, 0)      
        self.topBottom = self.ui_components.dual_input("Top-Bottom:", 0, 0)
                        
    def execute(self, imageBGRA):
        # get the height and width of the image
        h,w = imageBGRA.shape[:2]            

        # get the crop values from the input boxes
        leftCut, rightCut = self.ui_components.get_component_value(self.leftRight[:2], maxs=[w,w], defaults=[0, 0])
        topCut, bottomCut = self.ui_components.get_component_value(self.topBottom[:2], maxs=[h,h], defaults=[0, 0])
        
        # apply cropping
        imageBGRA = self.processor.crop(imageBGRA, leftCut, rightCut, topCut, bottomCut)  

        return imageBGRA    


class FlipBox(DraggableFunctionBox):
    """
    A box that allows the user to flip the image.
    This class provides a UI for specifying the flip angle and processes the image accordingly.
    """
    def __init__(self, parent=None):
        super().__init__(constants.FLIP_NAME, parent)

        # Create a radio button group to select the flip direction
        self.buttonGroup = self.ui_components.radio_buttons(["Horizontal", "Vertical", "Both"])

    def execute(self, imageBGRA):
        flipCodes = [1, 0, -1]          # horizontal, vertical, both

        # apply flipping
        imageBGRA = self.processor.flip(imageBGRA, flipCodes[self.buttonGroup[0].checkedId()])

        return imageBGRA
    

class RotateBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(constants.ROTATE_NAME, parent)

        # Create a slider to adjust the rotate angle
        self.angle = self.ui_components.slider(heading="Angle: ", minValue=-180, maxValue=180)  

    def execute(self, imageBGRA):
        # Get the current value of the slider
        value = self.angle[0].value()         

        # apply rotation
        imageBGRA = self.processor.rotate(imageBGRA, value)  

        return imageBGRA


class ResizeBox(DraggableFunctionBox):
    """
    A box that allows the user to resize the image.
    """
    def __init__(self, parent=None):
        super().__init__(constants.RESIZE_NAME, parent)

        # Create min and max input boxes for input size
        self.newWidthHeight  = self.ui_components.dual_input("Size:", 0, 0)
        
        # set a flag to check if the input size is set to default values
        self.init = False
                        
    def execute(self, imageBGRA):
        # get the height and width of the image
        (w, h) = imageBGRA.shape[:2]            

        # set the default values for the input boxes
        if not self.init:
            self.newWidthHeight[0].setText(str(w))
            self.newWidthHeight[1].setText(str(h))
            self.init = True

        # get input and output range values from the text boxes
        reWidth, reHeight = self.ui_components.get_component_value(self.newWidthHeight[:2], mins=[0, 0], defaults=[w, h])

        # apply resizing
        imageBGRA = self.processor.resize(imageBGRA, reWidth, reHeight)  

        return imageBGRA


class PaddingBox(DraggableFunctionBox):
    """
    A box that allows the user to add padding to the image.
    This class provides a UI for specifying the padding type and values.
    """
    def __init__(self, parent=None):
        super().__init__(constants.PADDING_NAME, parent)

        # Create  a combo list to select the padding type
        self.combo = self.ui_components.combo_list(["Constant", "Reflect", "Replicate"])

        # insert signle input box for constant value
        self.constant = self.ui_components.mono_input("Value:", defaultValue=0)
        
        # Create input boxes for padding amounts
        self.leftRight = self.ui_components.dual_input("Left-Right:", 0, 0)      
        self.topBottom = self.ui_components.dual_input("Top-Bottom:", 0, 0)

        # connect the combo box to the on_change function
        self.ui_components.set_combo_adapt_widgets(self.combo, [[self.constant, self.leftRight, self.topBottom], 
                                                                [self.leftRight, self.topBottom], [self.leftRight, self.topBottom]])

    def execute(self, imageBGRA):
        # get the padding type based on the selected combo box value
        padCodes = [cv2.BORDER_CONSTANT, cv2.BORDER_REFLECT, cv2.BORDER_REPLICATE]
        selectedId = self.combo.currentIndex()        
        paddingType = padCodes[selectedId]

        # get the constant value from input box
        constant = self.ui_components.get_component_value(self.constant[:1], mins=[0], maxs=[255], defaults=[0])

        # get the padding values from the input boxes
        lPad, rPad = self.ui_components.get_component_value(self.leftRight[:2], defaults=[0, 0])
        tPad, bPad = self.ui_components.get_component_value(self.topBottom[:2], defaults=[0, 0])

        # apply padding
        imageBGRA = self.processor.padding(imageBGRA, paddingType, lPad, rPad, tPad, bPad, constant)  

        return imageBGRA


class HistEqualizationBox(DraggableFunctionBox):
    """
    A box that performs histogram equalization on the image.
    This is a technique used to enhance the contrast of the image by redistributing the pixel intensity values.
    """
    def __init__(self, parent=None):
        super().__init__(constants.HISTEQ_NAME, parent)
  
    def execute(self, imageBGRA):
        # apply histogram equalization
        imageBGRA = self.processor.histogramEqualization(imageBGRA)  
        
        return imageBGRA


class HistCLAHEBox(DraggableFunctionBox):
    """
    CLAHE (Contrast Limited Adaptive Histogram Equalization) is a technique used to enhance the contrast of images.
    It is particularly useful for improving the visibility of details in images with varying lighting conditions.
    """
    def __init__(self, parent=None):
        super().__init__(constants.HISTCLAHE_NAME, parent)

        self.clipLimit_rescale = 10

        # create slider and input box for clip limit and tile grid size
        self.clipLimit = self.ui_components.slider(heading="Clip Limit:", minValue=1, maxValue=100, defaultValue=2, rescale=self.clipLimit_rescale)  
        self.tileGridSize = self.ui_components.mono_input("Tile Grid Size:", defaultValue=8)

    def execute(self, imageBGRA):
        # get the clip limit and tile grid size values
        clipLimit = self.clipLimit[0].value() / self.clipLimit_rescale
        tileGridSize = self.ui_components.get_component_value(self.tileGridSize[:1], mins=[4], maxs=[64], defaults=[8])
        tileGridSize = tileGridSize if tileGridSize % 2 == 0 else tileGridSize + 1          # allow only even numbers for tile grid size

        # apply CLAHE
        imageBGRA = self.processor.clahe(imageBGRA, clipLimit, tileGridSize)

        return imageBGRA
    

class MaskBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(constants.MASK_NAME, parent)

        # Create input boxes for mask range values
        self.intensityMin = self.ui_components.triple_input("min HSV:", 0, 0, 0)
        self.intensityMax = self.ui_components.triple_input("max HSV:", 0, 0, 0)

    def execute(self, imageBGRA):
        # get the mask range values from the input boxes
        rMin, gMin, bMin = self.ui_components.get_component_value(self.intensityMin[:3], mins=[0, 0, 0], maxs=[255,255, 255], defaults=[0, 0, 0])
        rMax, gMax, bMax = self.ui_components.get_component_value(self.intensityMax[:3], mins=[0, 0, 0], maxs=[255,255, 255], defaults=[0, 0, 0])

        # apply masking
        imageBGRA = self.processor.masking(imageBGRA, np.asarray([rMin, gMin, bMin]), np.asarray([rMax, gMax, bMax]))

        return imageBGRA
    

class BitSliceBox(DraggableFunctionBox):
    """
    A box that allows the user to select a bit plane from the image.
    This class provides a UI for specifying the bit plane and processes the image accordingly.
    """
    def __init__(self, parent=None):
        super().__init__(constants.BITSLICE_NAME, parent)

        # Create  a combo list to select a bit plane
        self.combo = self.ui_components.combo_list(["0", "1", "2", "3", "4", "5", "6", "7"])

    def execute(self, imageBGRA):
        # apply bit plane slicing
        imageBGRA = self.processor.bitSlice(imageBGRA, int(self.combo.currentText()))

        return imageBGRA


class NoiseBox(DraggableFunctionBox):
    """
    A box that allows the user to add noise to the image.
    This class provides a UI for specifying the noise type and parameters.
    """
    def __init__(self, parent=None):
        super().__init__(constants.ADD_NOISE_NAME, parent)

        self.saltPepProb_rescale = 1000

        # Create a combo list to select the noise type
        self.combo = self.ui_components.combo_list(["Gaussian", "Salt & Pepper", "Poisson"])

        # insert signle input boxes for mean and std values
        self.mean = self.ui_components.slider(heading="Mean:", minValue=-30, maxValue=300, defaultValue=0)
        self.std = self.ui_components.slider(heading="Std:", minValue=0, maxValue=100, defaultValue=25)

        # insert signle input boxes for salt and pepper values
        self.saltPepProb = self.ui_components.slider(heading="Probability:", minValue=0, maxValue=200, defaultValue=20, rescale=self.saltPepProb_rescale)

        # connect the combo box to the on_change function
        self.ui_components.set_combo_adapt_widgets(self.combo, [[self.mean, self.std], [self.saltPepProb], []])
   
    def execute(self, imageBGRA):
        if self.combo.currentText() == "Gaussian":
            # get mean and std values from the text boxes
            mean = self.mean[0].value() 
            std = self.std[0].value()

            # apply gaussian noise
            imageBGRA = self.processor.gaussianNoise(imageBGRA, mean, std)  
            
            return imageBGRA
        
        elif self.combo.currentText() == "Salt & Pepper":
            # get salt and pepper probability values from the text boxes
            saltPepProb = self.saltPepProb[0].value() / self.saltPepProb_rescale

            # apply salt and pepper noise
            imageBGRA = self.processor.saltPepperNoise(imageBGRA, saltPepProb)
            
            return imageBGRA    
        
        elif self.combo.currentText() == "Poisson": 
            # apply poisson noise
            imageBGRA = self.processor.poissonNoise(imageBGRA)
            
            return imageBGRA
   

class ArithmeticBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(constants.ARITHMETIC_NAME, parent)

        self.secondImage = None

        self.alpha_rescale = 100

        # insert a combo list to select the arithmetic operation
        self.combo = self.ui_components.combo_list(["Add", "Subtract", "Multiply", "Divide"])
        
        # insert a slider for alpha value
        self.alpha = self.ui_components.slider(heading="Alpha:", minValue=1, maxValue=1000, defaultValue=100, rescale=self.alpha_rescale)

        # insert a button to select the second image
        self.button = self.ui_components.button("Select Image")
        self.button[0].clicked.connect(self.select_image)  # connect the button to the select_image function

    def execute(self, imageBGRA):
        if self.secondImage is not None:
            alpha = self.alpha[0].value() / self.alpha_rescale           # get the alpha value from input box
            operation = self.combo.currentText()                # get the selected operation from combo box
            imageBGRA = self.processor.arithmetic(imageBGRA, self.secondImage, alpha, operation)  # apply arithmetic operation

        return imageBGRA
    
    
    def select_image(self):

        # Open file dialog to select an image file
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "Select an image file",
            "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp)"
        )

        if filePath:
            self.secondImage = cv2.imread(filePath, cv2.IMREAD_UNCHANGED)          # Read the image using OpenCV

            if len(self.secondImage.shape) == 2:  # if image is  (h,w)
                self.secondImage = cv2.cvtColor(self.secondImage, cv2.COLOR_GRAY2BGR)
            elif self.secondImage.shape[2] == 1:  # if image is (h,w,1)
                self.secondImage = cv2.cvtColor(self.secondImage, cv2.COLOR_GRAY2BGR)
            elif self.secondImage.shape[2] == 3:  # ig image is (BGR) (h,w,3)
                pass
            elif self.secondImage.shape[2] == 4:  # if image is (BGRA) (h,w,4)
                self.secondImage = self.secondImage[:, :, :3]  # remove the alpha channel

            self.on_change()        # emit the signal to indicate that the settings have been changed


class LogicBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(constants.LOGIC_NAME, parent)

        self.secondImage = None

        # insert a combo list to select the logic operation
        self.combo = self.ui_components.combo_list(["And", "Or", "Xor"])
        
        # insert a button to select the second image
        self.button = self.ui_components.button("Select Image")
        self.button[0].clicked.connect(self.select_image)  # connect the button to the select_image function

    def execute(self, imageBGRA):
        if self.secondImage is not None:
            operation = self.combo.currentText()                # get the selected operation from combo box
            imageBGRA = self.processor.logic(imageBGRA, self.secondImage, operation)  # apply logic operation

        return imageBGRA 

    
    def select_image(self):

        # Open file dialog to select an image file
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "Select an image file",
            "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp)"
        )

        if filePath:
            self.secondImage = cv2.imread(filePath, cv2.IMREAD_UNCHANGED)          # Read the image using OpenCV

            if len(self.secondImage.shape) == 2:  # if image is  (h,w)
                self.secondImage = cv2.cvtColor(self.secondImage, cv2.COLOR_GRAY2BGR)
            elif self.secondImage.shape[2] == 1:  # if image is (h,w,1)
                self.secondImage = cv2.cvtColor(self.secondImage, cv2.COLOR_GRAY2BGR)
            elif self.secondImage.shape[2] == 3:  # ig image is (BGR) (h,w,3)
                pass
            elif self.secondImage.shape[2] == 4:  # if image is (BGRA) (h,w,4)
                self.secondImage = self.secondImage[:, :, :3]  # remove the alpha channel

            self.on_change()        # emit the signal to indicate that the settings have been changed


class LaplaceBox(DraggableFunctionBox):
    """
    A box that performs laplace transformation on the image.
    """
    def __init__(self, parent=None):
        super().__init__(constants.LAPLACE_NAME, parent)

        # insert switch for extended laplace choice
        self.extended = self.ui_components.switch("Extended Laplace")
        
        # insert switch for normalize choice
        self.norm = self.ui_components.switch("Normalize")

    def execute(self, imageBGRA):
        # apply laplace transformation
        imageBGRA = self.processor.laplacian(imageBGRA, self.extended[0].isChecked(), self.norm[0].isChecked())  

        return imageBGRA


class SobelBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(constants.LAPLACE_NAME, parent)

        # insert switch for extended laplace choice
        self.norm = self.ui_components.switch("Normalize")
        
    def execute(self, imageBGRA):
        # apply sobel transformation
        imageBGRA = self.processor.sobel(imageBGRA, self.norm[0].isChecked())  

        return imageBGRA


class SpatialFilterBox(DraggableFunctionBox):
    """
    A box that allows the user to apply spatial filters to the image.
    This class provides a UI for specifying the filter type and parameters.
    """
    def __init__(self, parent=None):
        super().__init__(constants.SPATIAL_NAME, parent)

        self.alpha_rescale = 100
        self.sigma_rescale = 10

        # insert nedded widgets
        self.combo = self.ui_components.combo_list(["Median", "Max", "Min", "Mean", "Gaussian", "Laplace Sharpening", "Sobel Sharpening", "Unsharp Masking"])
        self.kernel = self.ui_components.mono_input("Kernel Size:", defaultValue=3)
        self.sigma = self.ui_components.slider(heading="Std:", minValue=1, maxValue=100, defaultValue=10, rescale=self.sigma_rescale)  
        self.extended = self.ui_components.switch("Extended Laplace")
        self.alpha = self.ui_components.slider(heading="Alpha:", minValue=1, maxValue=1000, defaultValue=100, rescale=self.alpha_rescale)

        # connect the combo box to the on_change function
        self.ui_components.set_combo_adapt_widgets(self.combo, [[self.kernel], [self.kernel], [self.kernel], [self.kernel],
                                                                 [self.kernel, self.sigma], [self.extended, self.alpha],
                                                                   [self.alpha], [self.kernel, self.sigma, self.alpha]])

    def execute(self, imageBGRA):
        w = self.ui_components.get_component_value(self.kernel[:1], mins=[0], defaults=[3])         # get the kernel size from input box
        w = w if w % 2 == 1 else w + 1                                      # make sure the kernel size is odd
        
        sigma = self.sigma[0].value() / self.sigma_rescale           # get the sigma value from input box
        alpha = self.alpha[0].value() / self.alpha_rescale       # get the alpha value from input box
        extended = self.extended[0].isChecked()    # get the extended laplace choice from switch

        if self.combo.currentText() == "Median":
            imageBGRA = self.processor.orderStatistics(imageBGRA, w, "median")  
        elif self.combo.currentText() == "Max":
            imageBGRA = self.processor.orderStatistics(imageBGRA, w, "max")  
        elif self.combo.currentText() == "Min":
            imageBGRA = self.processor.orderStatistics(imageBGRA, w, "min")  
        elif self.combo.currentText() == "Mean":
            imageBGRA = self.processor.boxFilter(imageBGRA, w)
        elif self.combo.currentText() == "Gaussian":
            imageBGRA = self.processor.gaussianBlur(imageBGRA, w, sigma)  
        elif self.combo.currentText() == "Laplace Sharpening":
            imageBGRA = self.processor.laplacianSharpening(imageBGRA, alpha, extended)
        elif self.combo.currentText() == "Sobel Sharpening":
            imageBGRA = self.processor.sobelSharpening(imageBGRA, alpha)
        elif self.combo.currentText() == "Unsharp Masking":
            imageBGRA = self.processor.unsharpMasking(imageBGRA, w, sigma, alpha)

        return imageBGRA
    
