import numpy as np
import cv2

from PySide6.QtCore import Qt, Slot, Signal, QMimeData
from PySide6.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame, QSlider,
                               QCheckBox, QComboBox, QFileDialog)
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
        newBtn.clicked.connect(self.addNewBox)
        self.frameLayout.addWidget(newBtn, alignment=Qt.AlignVCenter)

    @Slot()
    def addNewBox(self):
        """
        This function is called when the user clicks the "+" button.
        It emits a signal to indicate that a new function has been added.
        """
        # Get the selected function name from the combo box
        selected_function = self.combo.currentText()

        # Emit the trigger signal with the selected function name
        self.trigger.emit(selected_function)



class FunctionBox(QWidget):
    """
    A base class for creating function boxes in the GUI.
    This class provides a template for creating specific function boxes by subclassing it.
    """
    # Signals to communicate with the main application
    updateTrigger = Signal(str)
    removeTrigger = Signal(str)
   

    def __init__(self, title="Function", parent=None):
        super().__init__(parent)

        self.contentLayout = QVBoxLayout()
        self.processor = Processor()        # create an instance of the Processor class
        self.ui_components = UiComponents(parent=self.contentLayout, onchance_func=self.on_change)        # create an instance of the self.ui_components class

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
        self.switch.stateChanged.connect(self.on_change)
        self.switch.setFixedHeight(30)
        switchLayout.addWidget(self.switch, alignment=Qt.AlignTop)

        # add the content layout to the frame layout
        frameLayout.addLayout(self.contentLayout, 4)

        # add a dummy widget to fill the space
        dummy = QWidget()
        dummy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.contentLayout.addWidget(dummy)
    

    def execute(self):
        """
        This function is called to update the progress of the function.
        It should be overridden in subclasses to implement specific functionality.
        """
        pass


    def on_change(self):
        """
        This function is called when the user changes any settings in the function box.
        It should be overridden in subclasses to implement specific functionality.
        """
        self.updateTrigger.emit(self.title)




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
    A box that allows the user to adjust the brightness of image.
    """
    def __init__(self, parent=None):
        super().__init__(constants.BRIGHTNESS_NAME, parent)

        # Create a slider to adjust brightness
        self.brightness = self.ui_components.slider(heading="Brightness", minValue=-50, maxValue=50)  


    def execute(self, imageBGRA):
        """
        Adjusts the brightness of the given image based on the slider value.

        Args:
            image: The input image to be adjusted (e.g., a NumPy array or PIL Image).

        Returns:
            The brightness-adjusted image.
        """  
        # call the brightness function from Processors module
        imageBGRA = self.processor.brightness(imageBGRA, self.brightness[0].value())  

        return imageBGRA

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        It also updates the label with the current value of the slider.
        """
        # Update the label with the current value
        self.brightness[1].setText(f"Brightness: {self.brightness[0].value()}")
        
        super().on_change()



class SaturationBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(constants.SATURATION_NAME, parent)

        # Create a slider to adjust saturation
        self.saturation = self.ui_components.slider(heading="Saturation", minValue=-50, maxValue=50)


    def execute(self, imageBGRA):
        """
        """  
        value = self.saturation[0].value()                          # Get the current value of the slider
        imageBGRA = self.processor.saturation(imageBGRA, value)     # call the saturation function from Processors module

        return imageBGRA

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        It also updates the label with the current value of the slider.
        """
        # Update the label with the current value
        self.saturation[1].setText(f"Saturation: {self.saturation[0].value()}")
        
        super().on_change()



class ContrastBox(DraggableFunctionBox):
    """
    A box that allows the user to adjust the contrast of image.
    """
    def __init__(self, parent=None):
        super().__init__(constants.CONTRAST_NAME, parent)

        # create a combo list to select between input type (range or T(s))
        self.combo = self.ui_components.combo_list(["by Input-Output Range", "by T(s)"])

        # Create min and max input boxes for input range
        self.inMinMax = self.ui_components.dual_input("Input Range:")
        # Create min and max input boxes for output range
        self.outMinMax = self.ui_components.dual_input("Output Range:")

        # Create sliders for alpha and beta values
        self.alpha = self.ui_components.slider(heading="Alpha:", minValue=1, maxValue=30, defaultValue=10)
        self.beta = self.ui_components.slider(heading="Beta:", minValue=-50, maxValue=50)  
        
        # hide the input range boxes by default
        for x in self.alpha + self.beta:
            x.hide()   
                    
    def execute(self, imageBGRA):
        """
        Adjusts the contrast of the given image based on the input and output range values.
        """
        if self.combo.currentText() == "by Input-Output Range":
            # get input and output range values from the text boxes
            in_min, in_max = utils.GetWidgetValue(self.inMinMax[:2], maxs=[255,255], defaults=[0, 255])
            out_min, out_max = utils.GetWidgetValue(self.outMinMax[:2], maxs=[255,255], defaults=[0, 255])

            # call the contrast function from Processors module
            imageBGRA = self.processor.contrastByRange(imageBGRA, [in_min, in_max], [out_min, out_max])  

            return imageBGRA  

        elif self.combo.currentText() == "by T(s)":
            # get the alpha and beta values from sliders
            alpha = self.alpha[0].value()/10
            beta = self.beta[0].value()

            imageBGRA = self.processor.contrastByTS(imageBGRA, alpha, beta)  # call the contrast function from Processors module
            
            return imageBGRA

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """   
        # Update labels with current values
        self.alpha[1].setText(f"Alpha: {self.alpha[0].value()/10}")
        self.beta[1].setText(f"Beta: {self.beta[0].value()}")

        if self.combo.currentText() == "by Input-Output Range":
            # hide the alpha and beta input boxes and show the input range boxes
            for x in self.alpha + self.beta:
                x.hide()   
            for x in self.inMinMax + self.outMinMax:
                x.show()

        elif self.combo.currentText() == "by T(s)":
            # show the alpha and beta input boxes and hide the input range boxes
            for x in self.alpha + self.beta:
                x.show()   
            for x in self.inMinMax + self.outMinMax:
                x.hide()
                
        super().on_change()



class FullScaleContrastBox(DraggableFunctionBox):
    """
    A box that performs full scale contrast stretching on the image.
    """
    def __init__(self, parent=None):
        super().__init__(constants.FULL_SCALE_CONTRAST_NAME, parent)
  

    def execute(self, imageBGRA):
        """
        Performs full scale contrast stretching on the given image.
        This method adjusts the contrast of the image to span the full range of pixel values.
        """

        imageBGRA = self.processor.fullScaleContrast(imageBGRA)  # call the contrast function from Processors module
        
        return imageBGRA



class LogBox(DraggableFunctionBox):
    """
    A box that performs log transformation on the image.
    """
    def __init__(self, parent=None):
        super().__init__(constants.LOG_NAME, parent)
  

    def execute(self, imageBGRA):
        """
        Performs log transformation on the given image.
        This method applies a logarithmic transformation to the image to enhance the contrast of dark regions.
        """
        imageBGRA = self.processor.logTransform(imageBGRA)  # call the log function from Processors module

        return imageBGRA



class GammaBox(DraggableFunctionBox):
    """
    A box that performs gamma transformation on the image.
    This is a non-linear transformation that can be used to adjust the brightness and contrast of the image.
    """
    def __init__(self, parent=None):
        super().__init__(constants.GAMMA_NAME, parent)

        # insert signle input box for gamma value
        self.gamma = self.ui_components.slider(heading="Gamma:", minValue=1, maxValue=100, defaultValue=10)


    def execute(self, imageBGRA):
        """
        Performs gamma transformation on the given image.
        This method applies a gamma transformation to the image to adjust the brightness and contrast.
        """
        # get the threshold value from slider
        gamma = self.gamma[0].value()/10
        
        imageBGRA = self.processor.gammaTransform(imageBGRA, gamma)  # call the gamma function from Processors module

        return np.uint8(imageBGRA)     

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """       
        # Update the label with the current value
        self.gamma[1].setText(f"Gamma: {self.gamma[0].value()/10}")

        super().on_change()



class RGB2GrayBox(DraggableFunctionBox):
    """
    A box that converts image from RGB to grayscale.
    This class provides a UI for specifying the conversion and processes the image accordingly.
    """
    def __init__(self, parent=None):
        super().__init__(constants.RGB2GRAY_NAME, parent)
  

    def execute(self, imageBGRA):
        """
        Converts the given image from RGB to grayscale.
        This method transforms the image from RGB color space to grayscale.
        """
        imageBGRA = self.processor.rgb2gray(imageBGRA)              # call the rgb2gray function from Processors module

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
        """
        Converts the given image to black and white based on the threshold value.
        """
        # get the threshold value from slider
        threshold = self.threshold[0].value()                                       

        imageBGRA = self.processor.threshold(imageBGRA, threshold)          # call the threshold function from Processors module
        
        return imageBGRA


    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """    
        # Update the label with the current value
        self.threshold[1].setText(f"Threshold: {self.threshold[0].value()}")

        super().on_change()



class ComplementBox(DraggableFunctionBox):
    """
    A box that performs complememnt of image.
    This is a simple image processing operation that inverts the colors of the image.
    """
    def __init__(self, parent=None):
        super().__init__(constants.COMPLEMENT_NAME, parent)
  

    def execute(self, imageBGRA):
        """
        Performs complememnt of the given image.
        """
        imageBGRA = self.processor.complement(imageBGRA)  # call the complement function from Processors module

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
        """
        Crops the given image based on the input range values.
        """
        h,w = imageBGRA.shape[:2]            # get the height and width of the image

        # get the crop values from the input boxes
        leftCut, rightCut = utils.GetWidgetValue(self.leftRight[:2], maxs=[w,w], defaults=[0, 0])
        topCut, bottomCut = utils.GetWidgetValue(self.topBottom[:2], maxs=[h,h], defaults=[0, 0])
        
        imageBGRA = self.processor.crop(imageBGRA, leftCut, rightCut, topCut, bottomCut)  # call the crop function from Processors module

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
        """
        Flips the given image based on the slider value.
        """    
        flipCodes = [1, 0, -1]                          # horizontal, vertical, both
        imageBGRA = self.processor.flip(imageBGRA, flipCodes[self.buttonGroup.checkedId()])  

        return imageBGRA
    


class RotateBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(constants.ROTATE_NAME, parent)

        # Create a slider to adjust the rotate angle
        self.angle = self.ui_components.slider(heading="Angle: ", minValue=-180, maxValue=180)  


    def execute(self, imageBGRA):
        """
        Rotates the given image based on the slider value.
        This method rotates the image around its center by the specified angle.
        """        
        value = self.angle[0].value()         # Get the current value of the slider

        imageBGRA = self.processor.rotate(imageBGRA, value)  # call the rotate function from Processors module

        return imageBGRA

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        It also updates the label with the current value of the slider.
        """
        # Update the label with the current value
        self.angle[1].setText(f"Angle: {self.angle[0].value()}")
        
        super().on_change()



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
        """
        Resizes the given image based on the input size values.
        This method resizes the image to the specified width and height.
        """
        (w, h) = imageBGRA.shape[:2]            # get the height and width of the image

        # set the default values for the input boxes
        if not self.init:
            self.newWidthHeight[0].setText(str(w))
            self.newWidthHeight[1].setText(str(h))
            self.init = True

        # get input and output range values from the text boxes
        reWidth, reHeight = utils.GetWidgetValue(self.newWidthHeight[:2], mins=[0, 0], defaults=[w, h])

        imageBGRA = self.processor.resize(imageBGRA, reWidth, reHeight)  # call the resize function from Processors module

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
                        

    def execute(self, imageBGRA):
        """
        Applies padding to the given image based on the selected padding type and values.
        This method adds padding to the image using the specified padding type and values.
        """
        # get the padding type based on the selected combo box value
        padCodes = [cv2.BORDER_CONSTANT, cv2.BORDER_REFLECT, cv2.BORDER_REPLICATE]
        selectedId = self.combo.currentIndex()        
        paddingType = padCodes[selectedId]

        # get the constant value from input box
        constant = utils.GetWidgetValue(self.constant[:1], mins=[0], maxs=[255], defaults=[0])

        # get the padding values from the input boxes
        lPad, rPad = utils.GetWidgetValue(self.leftRight[:2], defaults=[0, 0])
        tPad, bPad = utils.GetWidgetValue(self.topBottom[:2], defaults=[0, 0])

        imageBGRA = self.processor.padding(imageBGRA, paddingType, lPad, rPad, tPad, bPad, constant)  # call the padding function from Processors module

        return imageBGRA
    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """    
        if self.combo.currentIndex() == 0:
            for x in self.constant:
                x.show()
        else:
            for x in self.constant:
                x.hide()

        super().on_change()



class HistEqualizationBox(DraggableFunctionBox):
    """
    A box that performs histogram equalization on the image.
    This is a technique used to enhance the contrast of the image by redistributing the pixel intensity values.
    """
    def __init__(self, parent=None):
        super().__init__(constants.HISTEQ_NAME, parent)
  

    def execute(self, imageBGRA):
        """
        Performs histogram equalization on the given image.
        This method enhances the contrast of the image by redistributing the pixel intensity values.
        """
        imageBGRA = self.processor.histogramEqualization(imageBGRA)  # call the histogram equalization function from Processors module
        
        return imageBGRA
    


class HistCLAHEBox(DraggableFunctionBox):
    """
    CLAHE (Contrast Limited Adaptive Histogram Equalization) is a technique used to enhance the contrast of images.
    It is particularly useful for improving the visibility of details in images with varying lighting conditions.
    """
    def __init__(self, parent=None):
        super().__init__(constants.HISTCLAHE_NAME, parent)

        # create slider and input box for clip limit and tile grid size
        self.clipLimit = self.ui_components.slider(heading="Clip Limit:", minValue=1, maxValue=100, defaultValue=2)  
        self.tileGridSize = self.ui_components.mono_input("Tile Grid Size:", defaultValue=8)

    def execute(self, imageBGRA):
        """
        Performs CLAHE on the given image.
        This method enhances the contrast of the image using the specified clip limit and tile grid size.
        """
        # get the clip limit and tile grid size values
        clipLimit = self.clipLimit[0].value()/10
        tileGridSize = utils.GetWidgetValue(self.tileGridSize[:1], mins=[4], maxs=[64], defaults=[8])
        tileGridSize = tileGridSize if tileGridSize % 2 == 0 else tileGridSize + 1          # allow only even numbers for tile grid size

        # call the CLAHE function from Processors module
        imageBGRA = self.processor.clahe(imageBGRA, clipLimit, tileGridSize)

        return imageBGRA
    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """   
        # Update the label with the current value
        self.clipLimit[1].setText(f"Clip Limit: {self.clipLimit[0].value()/10}")

        super().on_change()



class MaskBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(constants.MASK_NAME, parent)

        # Create input boxes for mask range values
        self.intensityMin = self.ui_components.triple_input("min HSV:", 0, 0, 0)
        self.intensityMax = self.ui_components.triple_input("max HSV:", 0, 0, 0)

    def execute(self, imageBGRA):
        """
        """
        # get the mask range values from the input boxes
        rMin, gMin, bMin = utils.GetWidgetValue(self.intensityMin[:3], mins=[0, 0, 0], maxs=[255,255, 255], defaults=[0, 0, 0])
        rMax, gMax, bMax = utils.GetWidgetValue(self.intensityMax[:3], mins=[0, 0, 0], maxs=[255,255, 255], defaults=[0, 0, 0])

        # call the mask function from Processors module
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
        """
        Extracts the selected bit plane from the given image.
        This method isolates the specified bit plane from the image and returns it as a binary image.
        """
        # call the bit slice function from Processors module
        imageBGRA = self.processor.bitSlice(imageBGRA, int(self.combo.currentText()))

        return imageBGRA



class NoiseBox(DraggableFunctionBox):
    """
    A box that allows the user to add noise to the image.
    This class provides a UI for specifying the noise type and parameters.
    """
    def __init__(self, parent=None):
        super().__init__(constants.ADD_NOISE_NAME, parent)

        # Create a combo list to select the noise type
        self.combo = self.ui_components.combo_list(["Gaussian", "Salt & Pepper", "Poisson"])

        # insert signle input boxes for mean and std values
        self.mean = self.ui_components.slider(heading="Mean:", minValue=-30, maxValue=300, defaultValue=0)
        self.std = self.ui_components.slider(heading="Std:", minValue=0, maxValue=100, defaultValue=25)

        # insert signle input boxes for salt and pepper values
        self.saltPepProb = self.ui_components.slider(heading="Probability:", minValue=0, maxValue=200, defaultValue=20)

        # hide the salt and pepper input boxes by default
        for x in self.saltPepProb:
            x.hide()    

    def execute(self, imageBGRA):
        """
        Adds noise to the given image based on the selected noise type and parameters.
        This method applies the specified noise to the image and returns the noisy image.
        """
        if self.combo.currentText() == "Gaussian":
            # get mean and std values from the text boxes
            mean = self.mean[0].value() 
            std = self.std[0].value()

            imageBGRA = self.processor.gaussianNoise(imageBGRA, mean, std)  # call the gaussian noise function from Processors module
            
            return imageBGRA
        
        elif self.combo.currentText() == "Salt & Pepper":
            # get salt and pepper probability values from the text boxes
            saltPepProb = self.saltPepProb[0].value() / 1000

            # call the salt and pepper noise function from Processors module
            imageBGRA = self.processor.saltPepperNoise(imageBGRA, saltPepProb)
            
            return imageBGRA    
        
        elif self.combo.currentText() == "Poisson": 
            # call the poisson noise function from Processors module
            imageBGRA = self.processor.poissonNoise(imageBGRA)
            
            return imageBGRA
    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """   
        # Update labels with current values
        self.mean[1].setText(f"Mean: {self.mean[0].value()}")
        self.std[1].setText(f"Std: {self.std[0].value()}")  

        self.saltPepProb[1].setText(f"Probability: {self.saltPepProb[0].value() / 1000}")

        if self.combo.currentText() == "Gaussian":
            # hide the salt and pepper input boxes and show the mean and std input boxes
            for x in self.mean + self.std:
                x.show()     
            for x in self.saltPepProb:
                x.hide()

        elif self.combo.currentText() == "Salt & Pepper":
            # hide the mean and std input boxes and show the salt and pepper input boxes
            for x in self.saltPepProb:
                x.show()
            for x in self.mean + self.std:
                x.hide()

        elif self.combo.currentText() == "Poisson": 
            # hide all the input boxes
            for x in self.saltPepProb:
                x.hide()
            for x in self.mean + self.std:
                x.hide()

        super().on_change()



class ArithmeticBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(constants.ARITHMETIC_NAME, parent)

        self.secondImage = None

        # insert a combo list to select the arithmetic operation
        self.combo = self.ui_components.combo_list(["Add", "Subtract", "Multiply", "Divide"])
        
        # insert a slider for alpha value
        self.alpha = self.ui_components.slider(heading="Alpha:", minValue=1, maxValue=1000, defaultValue=100)

        # insert a button to select the second image
        self.button = self.ui_components.button("Select Image")
        self.button.clicked.connect(self.select_image)  # connect the button to the select_image function

    def execute(self, imageBGRA):
        """
        """
        if self.secondImage is None:
            return imageBGRA
        
        alpha = self.alpha[0].value()/100           # get the alpha value from input box
        operation = self.combo.currentText()                # get the selected operation from combo box
        imageBGRA = self.processor.arithmetic(imageBGRA, self.secondImage, alpha, operation)  # call the arithmetic function from Processors module

        return imageBGRA
    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """    
        # Update the label with the current value
        self.alpha[1].setText(f"Alpha: {self.alpha[0].value()/100}")

        super().on_change()

    
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
        self.button.clicked.connect(self.select_image)  # connect the button to the select_image function

    def execute(self, imageBGRA):
        """
        """
        if self.secondImage is not None:
            operation = self.combo.currentText()                # get the selected operation from combo box
            imageBGRA = self.processor.logic(imageBGRA, self.secondImage, operation)  # call the logic function from Processors module

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
        """
        Performs laplace transformation on the given image.
        This method applies a laplace filter to the image to enhance the edges and details.
        """
        # call the laplace function from Processors module
        imageBGRA = self.processor.laplacian(imageBGRA, self.extended.isChecked(), self.norm.isChecked())  

        return imageBGRA



class SobelBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(constants.LAPLACE_NAME, parent)

        # insert switch for extended laplace choice
        self.norm = self.ui_components.switch("Normalize")
        

    def execute(self, imageBGRA):
        """
        """
        # call the sobel function from Processors module
        imageBGRA = self.processor.sobel(imageBGRA, self.norm.isChecked())  

        return imageBGRA



class SpatialFilterBox(DraggableFunctionBox):
    """
    A box that allows the user to apply spatial filters to the image.
    This class provides a UI for specifying the filter type and parameters.
    """
    def __init__(self, parent=None):
        super().__init__(constants.SPATIAL_NAME, parent)

        # create a combo list to select spatial filter type
        self.combo = self.ui_components.combo_list(["Median", "Max", "Min", "Mean", "Gaussian", "Laplace Sharpening", "Sobel Sharpening", "Unsharp Masking"])

        # insert a signle input box for kernel size
        self.kernel = self.ui_components.mono_input("Kernel Size:", defaultValue=3)

        # create a slider for sigma value
        self.sigma = self.ui_components.slider(heading="Std:", minValue=0, maxValue=50, defaultValue=1)  
        # hide the sigma slider by default
        for x in self.sigma:
            x.hide()

        # insert a switch for extended laplace choice
        self.extended = self.ui_components.switch("Extended Laplace")
        self.extended.hide()  # hide the switch by default

        # insert a slider for alpha value
        self.alpha = self.ui_components.slider(heading="Alpha:", minValue=1, maxValue=1000, defaultValue=100)
        # hide the alpha input box by default
        for x in self.alpha:
            x.hide()  


    def execute(self, imageBGRA):
        """
        Applies the selected spatial filter to the given image based on the specified parameters.
        This method processes the image using the selected filter type and parameters.
        """
        w = utils.GetWidgetValue(self.kernel[:1], mins=[0], defaults=[3])         # get the kernel size from input box
        w = w if w % 2 == 1 else w + 1                                      # make sure the kernel size is odd
        
        sigma = self.sigma[0].value()           # get the sigma value from input box
        alpha = self.alpha[0].value()/100       # get the alpha value from input box
        extended = self.extended.isChecked()    # get the extended laplace choice from switch

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

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """    
        # Update the label with the current value
        self.sigma[1].setText(f"Std: {self.sigma[0].value()}")
        self.alpha[1].setText(f"Alpha: {self.alpha[0].value()/100}")

        if self.combo.currentText() == "Mean" or self.combo.currentText() == "Median" or self.combo.currentText() == "Max" or self.combo.currentText() == "Min":
            for x in self.kernel:
                x.show()
            for x in self.sigma + self.alpha:
                x.hide()   
            self.extended.hide()
        elif self.combo.currentText() == "Gaussian":
            for x in self.kernel:
                x.show()
            for x in self.sigma:
                x.show()     
            for x in self.alpha:
                x.hide() 
            self.extended.hide()
        elif self.combo.currentText() == "Laplace Sharpening":
            for x in self.kernel + self.sigma:
                x.hide()     
            for x in self.alpha:
                x.show() 
            self.extended.show()
        elif self.combo.currentText() == "Sobel Sharpening":
            for x in self.kernel + self.sigma:
                x.hide()     
            for x in self.alpha:
                x.show()
            self.extended.hide()
        elif self.combo.currentText() == "Unsharp Masking":
            for x in self.kernel:
                x.show()
            for x in self.sigma:
                x.show()     
            for x in self.alpha:
                x.show()
            self.extended.hide()

        super().on_change()

