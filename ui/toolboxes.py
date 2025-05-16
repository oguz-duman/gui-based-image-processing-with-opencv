import numpy as np
import cv2

from PySide6.QtCore import Qt, Signal, QMimeData
from PySide6.QtGui import QFont, QDrag
from PySide6.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, 
                               QSizePolicy, QFrame, QCheckBox, QComboBox)

from processing.processor import Processor
from ui.components import UiComponents 
import constants
from ui.ui_management import UiManagement


class AddNewBox(QWidget):
    """
    A widget that allows the user to add new toolboxes.
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
        label = QLabel(constants.ADD_TOOLBOX_TITLE)
        label.setFont(self.font)
        label.setAlignment(Qt.AlignHCenter)
        self.frameLayout.addWidget(label)
        
        # Create a combo box to select the function type
        self.combo = QComboBox()
        self.combo.addItems(constants.FUNCTION_NAMES)
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
    A base class for all toolboxes. It provides a common interface.
    Parameters:
        title (str): The title of the toolbox.
        parent (QWidget): The parent widget where the toolbox will be added.
    """
    # Signals to communicate with the main application
    updateTrigger = Signal()
    removeTrigger = Signal(str)
   

    def __init__(self, title="Function", parent=None):
        super().__init__(parent)


        self.contentLayout = QVBoxLayout()      # create a layout to hold the content of the toolbox

        self.processor = Processor()            # create an instance of the Processor class to get the image processing functions
        # create an instance of the self.ui_components class to create the UI components
        self.ui_components = UiComponents(parent_widget=self.contentLayout, onchange_trigger=self.updateTrigger)        
        
        self.title = title                      # set the title of the function box
        self.initiate_ui()                 # set up the UI


    def initiate_ui(self):
        """
        Initiate the UI for the function box.
        """
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
        label = QLabel(self.title)
        label.setFont(self.font)
        titleLayout.addWidget(label)

        # create a button to remove the function box
        removeBtn = QPushButton("X")
        removeBtn.setFont(self.font)
        removeBtn.setFixedWidth(30)
        removeBtn.clicked.connect(lambda: self.removeTrigger.emit(self.title))
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
    """
    A base class for all toolboxes that can be dragged and dropped.
    """
    def mousePressEvent(self, event):
        """
        Handles the mouse press event to initiate dragging.
        Stores the starting position of the drag when the left mouse button is pressed.
        """
        if event.button() == Qt.LeftButton:
            self.dragStartPosition = event.position()

    def mouseMoveEvent(self, event):
        """
        Handles the mouse move event to perform dragging.
        Initiates a drag operation if the left mouse button is held and the mouse is moved beyond a threshold.
        """
        # Check if the left mouse button is pressed
        if not event.buttons() & Qt.LeftButton:
            return
        # Check if the mouse has moved beyond a small threshold
        if (event.position() - self.dragStartPosition).manhattanLength() < 10:
            return

        drag = QDrag(self)                              # Create a QDrag object to handle the drag operation
        mimeData = QMimeData()                          # Create a QMimeData object to store data for the drag
        drag.setMimeData(mimeData)                      
        drag.setHotSpot(event.position().toPoint())     # Set the hotspot for the drag operation
        drag.setPixmap(self.grab())                     # # Set the pixmap for the drag operation (visual representation)
        drag.exec(Qt.MoveAction)                        # Execute the drag operation with a move action



class BrightnessBox(DraggableFunctionBox):
    """
    A class to create a brightness adjustment toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.BRIGHTNESS_NAME, parent)

        # Create a slider to adjust brightness
        self.brightness = self.ui_components.slider(heading="Brightness", minValue=-50, maxValue=50)  

    def execute(self, imageBGRA):
        # apply brightness adjustment
        imageBGRA = self.processor.brightness(imageBGRA, self.brightness[0].value())  

        return imageBGRA


class SaturationBox(DraggableFunctionBox):
    """
    A class to create a saturation adjustment toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.SATURATION_NAME, parent)

        # Create a slider to adjust saturation
        self.saturation = self.ui_components.slider(heading="Saturation", minValue=-50, maxValue=50)

    def execute(self, imageBGRA):
        # apply saturation adjustment
        imageBGRA = self.processor.saturation(imageBGRA, self.saturation[0].value())     

        return imageBGRA


class ContrastBox(DraggableFunctionBox):
    """
    A class to create a contrast adjustment toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.CONTRAST_NAME, parent)

        self.slider_rescale = 10    # set a rescale factor for the slider

        # insert a combo list to select between input type (range or T(s))
        self.combo = self.ui_components.combo_list(["by Input-Output Range", "by T(s)"])

        # insert min-max input boxes for input and output range
        self.inMinMax = self.ui_components.dual_input("Input Range:")
        self.outMinMax = self.ui_components.dual_input("Output Range:")

        # insert sliders for alpha and beta values
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
            imageBGRA = self.processor.contrast_by_range(imageBGRA, [in_min, in_max], [out_min, out_max])  

            return imageBGRA  

        elif self.combo.currentText() == "by T(s)":
            # get the alpha and beta values from sliders
            alpha = self.alpha[0].value() / self.slider_rescale
            beta = self.beta[0].value()

            # apply contrast stretching using T(s) method
            imageBGRA = self.processor.contrast_by_T(imageBGRA, alpha, beta)  
            
            return imageBGRA
              

class FullScaleContrastBox(DraggableFunctionBox):
    """
    A class to create a full scale contrast adjustment toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.FULL_SCALE_CONTRAST_NAME, parent)
  
    def execute(self, imageBGRA):
        # apply full scale contrast stretching
        imageBGRA = self.processor.full_scale_contrast(imageBGRA)  
        
        return imageBGRA


class LogBox(DraggableFunctionBox):
    """
    A class to create a log transformation toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.LOG_NAME, parent)
  
    def execute(self, imageBGRA):
        # apply log transformation
        imageBGRA = self.processor.log_transform(imageBGRA)  

        return imageBGRA


class GammaBox(DraggableFunctionBox):
    """
    A class to create a gamma transformation toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.GAMMA_NAME, parent)

        self.slider_rescale = 10        # set a rescale factor for the slider

        # insert signle input box to select the gamma value
        self.gamma = self.ui_components.slider(heading="Gamma:", minValue=1, maxValue=100, defaultValue=10, rescale=self.slider_rescale)

    def execute(self, imageBGRA):
        gamma = self.gamma[0].value() / self.slider_rescale             # get the threshold value from slider
        imageBGRA = self.processor.gamma_transform(imageBGRA, gamma)    # apply gamma transformation

        return np.uint8(imageBGRA)     


class RGB2GrayBox(DraggableFunctionBox):
    """
    A class to create a RGB to grayscale conversion toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.RGB2GRAY_NAME, parent)

    def execute(self, imageBGRA):
        # apply RGB to grayscale conversion
        imageBGRA = self.processor.rgb2gray(imageBGRA)              

        return imageBGRA


class ThresholdingBox(DraggableFunctionBox):
    """
    A class to create a thresholding toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.THRESHOLDING_NAME, parent)

        # insert slider to select the threshold value
        self.threshold = self.ui_components.slider(heading="Threshold:", minValue=0, maxValue=255, defaultValue=128)

    def execute(self, imageBGRA):
        threshold = self.threshold[0].value()                               # get the threshold value from slider
        imageBGRA = self.processor.threshold(imageBGRA, threshold)          # apply thresholding
        
        return imageBGRA


class ComplementBox(DraggableFunctionBox):
    """
    A class to create a complement toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.COMPLEMENT_NAME, parent)
  
    def execute(self, imageBGRA):
        imageBGRA = self.processor.complement(imageBGRA)    # apply complement operation

        return imageBGRA


class CropBox(DraggableFunctionBox):
    """
    A class to create a cropping toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.CROP_NAME, parent)

        # Insert input boxes to select the crop values
        self.leftRight  = self.ui_components.dual_input("Left-Right:", 0, 0)      
        self.topBottom = self.ui_components.dual_input("Top-Bottom:", 0, 0)
                        
    def execute(self, imageBGRA):
        h,w = imageBGRA.shape[:2]       # get the height and width of the input image

        # get the crop values from input
        leftCut, rightCut = self.ui_components.get_component_value(self.leftRight[:2], maxs=[w,w], defaults=[0, 0])
        topCut, bottomCut = self.ui_components.get_component_value(self.topBottom[:2], maxs=[h,h], defaults=[0, 0])
        
        # apply cropping
        imageBGRA = self.processor.crop(imageBGRA, leftCut, rightCut, topCut, bottomCut)  

        return imageBGRA    


class FlipBox(DraggableFunctionBox):
    """
    A class to create a flipping toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.FLIP_NAME, parent)

        # Insert a radio button group to select the flip direction
        self.buttonGroup = self.ui_components.radio_buttons(["Horizontal", "Vertical", "Both"])

    def execute(self, imageBGRA):
        flipCodes = [1, 0, -1]          # horizontal, vertical, both
        imageBGRA = self.processor.flip(imageBGRA, flipCodes[self.buttonGroup[0].checkedId()])  # apply flipping

        return imageBGRA
    

class RotateBox(DraggableFunctionBox):
    """
    A class to create a rotation toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.ROTATE_NAME, parent)

        # Insert a slider to adjust the rotate angle
        self.angle = self.ui_components.slider(heading="Angle: ", minValue=-180, maxValue=180)  

    def execute(self, imageBGRA):
        value = self.angle[0].value()                           # Get the current value of the slider
        imageBGRA = self.processor.rotate(imageBGRA, value)     # apply rotation

        return imageBGRA


class ResizeBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(constants.RESIZE_NAME, parent)

        # Insert min-max input boxes to select the new size
        self.newWidthHeight  = self.ui_components.dual_input("Size:", 0, 0)
        
        self.init = False       # set a flag to check if the inputs are set to the image size as default
                        
    def execute(self, imageBGRA):
        (w, h) = imageBGRA.shape[:2]        # get the height and width of the image

        # set the input boxes to the image size as default
        if not self.init:
            self.newWidthHeight[0].setText(str(w))
            self.newWidthHeight[1].setText(str(h))
            self.init = True

        # get input and output range values from the text boxes and apply resizing
        reWidth, reHeight = self.ui_components.get_component_value(self.newWidthHeight[:2], mins=[0, 0], defaults=[w, h])
        imageBGRA = self.processor.resize(imageBGRA, reWidth, reHeight)  

        return imageBGRA


class PaddingBox(DraggableFunctionBox):
    """
    A class to create a padding toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.PADDING_NAME, parent)

        # Insert a combo list to select the padding type
        self.combo = self.ui_components.combo_list(["Constant", "Reflect", "Replicate"])

        # Insert a signle input box to select the constant value
        self.constant = self.ui_components.mono_input("Value:", defaultValue=0)
        
        # Insert input boxes to select the padding values
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

        # get the input values from the input boxes
        constant = self.ui_components.get_component_value(self.constant[:1], mins=[0], maxs=[255], defaults=[0])
        lPad, rPad = self.ui_components.get_component_value(self.leftRight[:2], defaults=[0, 0])
        tPad, bPad = self.ui_components.get_component_value(self.topBottom[:2], defaults=[0, 0])

        # apply padding
        imageBGRA = self.processor.padding(imageBGRA, paddingType, lPad, rPad, tPad, bPad, constant)  

        return imageBGRA


class HistEqualizationBox(DraggableFunctionBox):
    """
    A class to create a histogram equalization toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.HISTEQ_NAME, parent)
  
    def execute(self, imageBGRA):
        # apply histogram equalization
        imageBGRA = self.processor.histogram_equalization(imageBGRA)  
        
        return imageBGRA


class HistCLAHEBox(DraggableFunctionBox):
    """
    A class to create a histogram CLAHE toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.HISTCLAHE_NAME, parent)

        self.clipLimit_rescale = 10     # set a rescale factor for the slider

        # Insert a slider and input box to select the clip limit and tile grid size
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
    A class to create a masking toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.MASK_NAME, parent)

        # Insert input boxes to select the min-max HSV values
        self.intensityMin = self.ui_components.triple_input("min HSV:", 0, 0, 0)
        self.intensityMax = self.ui_components.triple_input("max HSV:", 0, 0, 0)

    def execute(self, imageBGRA):
        # get the min-max HSV values from the input boxes
        rMin, gMin, bMin = self.ui_components.get_component_value(self.intensityMin[:3], mins=[0, 0, 0], maxs=[255,255, 255], defaults=[0, 0, 0])
        rMax, gMax, bMax = self.ui_components.get_component_value(self.intensityMax[:3], mins=[0, 0, 0], maxs=[255,255, 255], defaults=[0, 0, 0])

        # apply masking
        imageBGRA = self.processor.masking(imageBGRA, np.asarray([rMin, gMin, bMin]), np.asarray([rMax, gMax, bMax]))

        return imageBGRA
    

class BitSliceBox(DraggableFunctionBox):
    """
    A class to create a bit plane slicing toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.BITSLICE_NAME, parent)

        # Insert a combo list to select a bit plane
        self.combo = self.ui_components.combo_list(["0", "1", "2", "3", "4", "5", "6", "7"])

    def execute(self, imageBGRA):
        # apply bit plane slicing
        imageBGRA = self.processor.bit_slice(imageBGRA, int(self.combo.currentText()))

        return imageBGRA


class NoiseBox(DraggableFunctionBox):
    """
    A class to create a noise toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.ADD_NOISE_NAME, parent)

        self.saltPepProb_rescale = 1000         # set a rescale factor for the slider

        # Insert a combo list to select the noise type
        self.combo = self.ui_components.combo_list(["Gaussian", "Salt & Pepper", "Poisson"])

        # insert signle input boxes to select the mean and std values
        self.mean = self.ui_components.slider(heading="Mean:", minValue=-30, maxValue=300, defaultValue=0)
        self.std = self.ui_components.slider(heading="Std:", minValue=0, maxValue=100, defaultValue=25)

        # insert signle input boxes to select the salt and pepper probability
        self.saltPepProb = self.ui_components.slider(heading="Probability:", minValue=0, maxValue=200, defaultValue=20, rescale=self.saltPepProb_rescale)

        # connect the combo box to the on_change function
        self.ui_components.set_combo_adapt_widgets(self.combo, [[self.mean, self.std], [self.saltPepProb], []])
   
    def execute(self, imageBGRA):
        if self.combo.currentText() == "Gaussian":
            # get mean and std values from inputs and apply gaussian noise
            mean = self.mean[0].value() 
            std = self.std[0].value()
            imageBGRA = self.processor.gaussian_noise(imageBGRA, mean, std)  
            
            return imageBGRA
        
        elif self.combo.currentText() == "Salt & Pepper":
            # get salt and pepper probability values from the text boxes and apply salt and pepper noise
            saltPepProb = self.saltPepProb[0].value() / self.saltPepProb_rescale
            imageBGRA = self.processor.salt_pepper_noise(imageBGRA, saltPepProb)
            
            return imageBGRA    
        
        elif self.combo.currentText() == "Poisson": 
            # apply poisson noise
            imageBGRA = self.processor.poisson_noise(imageBGRA)
            
            return imageBGRA
   

class ArithmeticBox(DraggableFunctionBox):
    """
    A class to create an arithmetic operation toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.ARITHMETIC_NAME, parent)

        self.secondImage = None         # set a variable to store the second image
        self.alpha_rescale = 100        # set a rescale factor for the slider

        # insert a combo list to select the arithmetic operation
        self.combo = self.ui_components.combo_list(["Add", "Subtract", "Multiply", "Divide"])
        
        # insert a slider to select the alpha value
        self.alpha = self.ui_components.slider(heading="Alpha:", minValue=1, maxValue=1000, defaultValue=100, rescale=self.alpha_rescale)

        # insert a button to select a new second image
        self.button = self.ui_components.button("Select Image")
        self.button[0].clicked.connect(self.open_second_image_button)  # connect the button click to the open_second_image_button function

    def execute(self, imageBGRA):
        if self.secondImage is not None:
            alpha = self.alpha[0].value() / self.alpha_rescale                      # get the alpha value from input 
            operation = self.combo.currentText()                                    # get the selected operation from combo box
            imageBGRA = self.processor.arithmetic(imageBGRA, self.secondImage, alpha, operation)  # apply arithmetic operation

        return imageBGRA
    
    def open_second_image_button(self):
        """
        Open a file dialog to select the second image.
        """
        imageBGRA = UiManagement.select_image(None)     # read the image

        if imageBGRA is not None:
            self.secondImage = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)  # convert the image to BGR format
            self.on_change()        # emit the signal to indicate that the settings have been changed



class LogicBox(DraggableFunctionBox):
    """
    A class to create a logic operation toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.LOGIC_NAME, parent)

        self.secondImage = None         # set a variable to store the second image

        # insert a combo list to select the logic operation
        self.combo = self.ui_components.combo_list(["And", "Or", "Xor"])
        
        # insert a button to select the second image
        self.button = self.ui_components.button("Select Image")
        self.button[0].clicked.connect(self.open_second_image_button)  # connect the button click to the open_second_image_button function


    def execute(self, imageBGRA):
        if self.secondImage is not None:
            operation = self.combo.currentText()                                        # get the selected operation from combo box
            imageBGRA = self.processor.logic(imageBGRA, self.secondImage, operation)    # apply logic operation

        return imageBGRA 

    def open_second_image_button(self):
        """
        Open a file dialog to select the second image.
        """
        imageBGRA = UiManagement.select_image(None)     # read the image

        if imageBGRA is not None:
            self.secondImage = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)  # convert the image to BGR format
            self.on_change()        # emit the signal to indicate that the settings have been changed



class LaplaceBox(DraggableFunctionBox):
    """
    A class to create a laplace transformation toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.LAPLACE_NAME, parent)

        # insert switch to select extended laplace and normalize options
        self.extended = self.ui_components.switch("Extended Laplace")
        self.norm = self.ui_components.switch("Normalize")

    def execute(self, imageBGRA):
        # apply laplace transformation
        imageBGRA = self.processor.laplacian(imageBGRA, self.extended[0].isChecked(), self.norm[0].isChecked())  

        return imageBGRA


class SobelBox(DraggableFunctionBox):
    """
    A class to create a sobel transformation toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.LAPLACE_NAME, parent)

        # insert a switch to select the normalize option
        self.norm = self.ui_components.switch("Normalize")
        
    def execute(self, imageBGRA):
        # apply sobel transformation
        imageBGRA = self.processor.sobel(imageBGRA, self.norm[0].isChecked())  

        return imageBGRA


class SpatialFilterBox(DraggableFunctionBox):
    """
    A class to create a spatial filter toolbox.
    """
    def __init__(self, parent=None):
        super().__init__(constants.SPATIAL_NAME, parent)

        # set rescale factors for sliders
        self.alpha_rescale = 100
        self.sigma_rescale = 10

        # insert nedded input widgets
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
        # get the kernel size and make sure it is odd
        w = self.ui_components.get_component_value(self.kernel[:1], mins=[0], defaults=[3])         
        w = w if w % 2 == 1 else w + 1                                      
        
        # get the sigma, alpha and extended laplace values from inputs
        sigma = self.sigma[0].value() / self.sigma_rescale      
        alpha = self.alpha[0].value() / self.alpha_rescale      
        extended = self.extended[0].isChecked()                 
        
        # apply the selected spatial filter
        if self.combo.currentText() == "Median":
            imageBGRA = self.processor.order_statistics(imageBGRA, w, "median")  
        elif self.combo.currentText() == "Max":
            imageBGRA = self.processor.order_statistics(imageBGRA, w, "max")  
        elif self.combo.currentText() == "Min":
            imageBGRA = self.processor.order_statistics(imageBGRA, w, "min")  
        elif self.combo.currentText() == "Mean":
            imageBGRA = self.processor.box_filter(imageBGRA, w)
        elif self.combo.currentText() == "Gaussian":
            imageBGRA = self.processor.gaussian_blur(imageBGRA, w, sigma)  
        elif self.combo.currentText() == "Laplace Sharpening":
            imageBGRA = self.processor.laplacian_sharpening(imageBGRA, alpha, extended)
        elif self.combo.currentText() == "Sobel Sharpening":
            imageBGRA = self.processor.sobel_sharpening(imageBGRA, alpha)
        elif self.combo.currentText() == "Unsharp Masking":
            imageBGRA = self.processor.unsharp_masking(imageBGRA, w, sigma, alpha)

        return imageBGRA
    
