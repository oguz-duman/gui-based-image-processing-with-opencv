import numpy as np
import cv2

from PySide6.QtCore import Qt, Slot, Signal, QMimeData
from PySide6.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame, QSlider, 
                               QCheckBox, QComboBox, QLineEdit, QRadioButton, QButtonGroup, QFileDialog)
from PySide6.QtGui import QFont, QDrag


# function names
BRIGHTNESS_NAME = "Brightness"
CONTRAST_NAME = "Contrast"
FULL_SCALE_CONTRAST_NAME = "Full Scale Contrast"
LOG_NAME = "Log Transform"
GAMMA_NAME = "Gamma Transform"
BLACK_AND_WHITE_NAME = "Black and White"
COMPLEMENT_NAME = "Complement"
CROP_NAME = "Crop"
FLIP_NAME = "Flip"
ROTATE_NAME = "Rotate"
RESIZE_NAME = "Resize"
PADDING_NAME = "Padding"
HISTEQ_NAME = "Histogram Equalization"
HISTCLAHE_NAME = "Local Hist. Equalization"
BITSLICE_NAME = "Bit Plane Slicing"
ADD_NOISE_NAME = "Add Noise"
RGB2GRAY_NAME = "RGB to Gray"
ARITHMETIC_NAME = "Image Arithmetic"
LAPLACE_NAME = "Laplacian Filter"
SOBEL_NAME = "Sobel Filter"
SPATIAL_NAME = "Spatial Filter"

# list of function names to use in combo box
function_names = [BRIGHTNESS_NAME, CONTRAST_NAME, FULL_SCALE_CONTRAST_NAME, LOG_NAME, GAMMA_NAME, BLACK_AND_WHITE_NAME, 
                  COMPLEMENT_NAME, CROP_NAME, FLIP_NAME, ROTATE_NAME, RESIZE_NAME, PADDING_NAME, HISTEQ_NAME, HISTCLAHE_NAME,
                  BITSLICE_NAME, ADD_NOISE_NAME, RGB2GRAY_NAME, ARITHMETIC_NAME, LAPLACE_NAME, SOBEL_NAME, SPATIAL_NAME]


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
        self.combo.addItems(function_names)
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

        # set the title of the function box
        self.title = title

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

        if title != "Add New":

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
        
        else:
            titleLayout.setAlignment(Qt.AlignHCenter)

        # create a content layout for the function features
        self.contentLayout = QVBoxLayout()
        frameLayout.addLayout(self.contentLayout, 4)

        # add a dummy widget to fill the space
        dummy = QWidget()
        dummy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.contentLayout.addWidget(dummy)
        

        # call the build_ui method to add specific UI elements
        self.build_ui()


    def build_ui(self):
        """
        This function is called to build the UI elements of the function box.
        It should be overridden in subclasses to implement specific functionality.
        """
        pass


    def process(self):
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



    def InsertSlider(self, heading, minValue, maxValue, defaultValue=0):

        """
        This function is called to insert a slider into the function box.
        """
        # Create a label to display the current value of the slider
        label = QLabel(f"{heading}: 0")
        label.setFont(self.font)
        self.contentLayout.addWidget(label, alignment=Qt.AlignLeft)

        # Create a slider to adjust brightness
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(minValue)
        slider.setMaximum(maxValue)
        slider.setValue(defaultValue)
        slider.valueChanged.connect(self.on_change)
        self.contentLayout.addWidget(slider)

        return slider, label


    def InsertMinMax(self, heading, defaultMin=0, defaultMax=255):
        """
        This function is called to insert min and max input boxes into the function box.
        """
        # Input range area
        layout1 = QHBoxLayout()
        self.contentLayout.addLayout(layout1)

        # an indicator for input range
        inLabel = QLabel(heading)
        inLabel.setFont(self.font)
        layout1.addWidget(inLabel)

        # min value for input range 
        inRangeMin = QLineEdit()
        inRangeMin.setFont(self.font)
        inRangeMin.setText(str(defaultMin))
        inRangeMin.setFixedWidth(40)
        inRangeMin.textChanged.connect(self.on_change)
        layout1.addWidget(inRangeMin)

        # max value for input range
        inRangeMax = QLineEdit()
        inRangeMax.setFont(self.font)
        inRangeMax.setText(str(defaultMax))
        inRangeMax.setFixedWidth(40)
        inRangeMax.textChanged.connect(self.on_change)
        layout1.addWidget(inRangeMax)

        return [inRangeMin, inRangeMax, inLabel]
    

    def InsertSingleInput(self, heading, defaultValue=0):
        """
        This function is called to insert a single input box into the function box.
        """

        # layout for the input box
        layout = QHBoxLayout()
        self.contentLayout.addLayout(layout)

        # heading for the input
        label = QLabel(heading)
        label.setFont(self.font)
        layout.addWidget(label, alignment=Qt.AlignLeft)

        # input box for the value 
        inArea = QLineEdit()
        inArea.setFont(self.font)
        inArea.setText(str(defaultValue))
        inArea.setFixedWidth(40)
        inArea.textChanged.connect(self.on_change)
        layout.addWidget(inArea, alignment=Qt.AlignLeft)

        return [inArea, label]
    
    
    def InsertRadioButtons(self, headings=[]):
        """
        This function is called to insert radio buttons into the function box.
        It creates a vertical layout for the radio buttons and adds them to the content layout.
        """
        # layout for radio buttons
        layout = QVBoxLayout()
        self.contentLayout.addLayout(layout)

        # create a button group to hold the radio buttons
        buttonGroup = QButtonGroup(self)  
        buttonGroup.buttonClicked.connect(self.on_change)      

        # create radio buttons
        for i, heading in enumerate(headings):
            radio = QRadioButton(heading)
            buttonGroup.addButton(radio, i)            
            radio.setFont(self.font)
            layout.addWidget(radio, alignment=Qt.AlignLeft)
        
        # click the first button by default
        if buttonGroup.buttons():
            buttonGroup.buttons()[0].setChecked(True)

        return buttonGroup


    def InsertComboList(self, headings=[]):
        """
        This function is called to insert a combo box into the function box.
        """
        combo = QComboBox()
        combo.addItems(headings)
        combo.setFont(self.font)
        combo.currentIndexChanged.connect(self.on_change)       # onchange event for the combo box
        self.contentLayout.addWidget(combo)                     # add the combo box to the content layout

        return combo

    def InsertSwitch(self, heading):
        """
        This function is called to insert a switch into the function box.
        """
        onOff = QCheckBox(heading)
        onOff.setChecked(False)
        onOff.setFont(self.font)
        onOff.stateChanged.connect(self.on_change)
        onOff.setFixedHeight(30)
        self.contentLayout.addWidget(onOff)

        return onOff

    def InsertButton(self, heading):
        """
        This function is called to insert a button into the function box.
        """
        button = QPushButton(heading)
        button.setFont(self.font)
        button.setFixedHeight(30)
        self.contentLayout.addWidget(button)

        return button



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
        super().__init__(BRIGHTNESS_NAME, parent)

    def build_ui(self):
        # Create a slider to adjust brightness
        self.slider, self.label = self.InsertSlider(heading="Brightness", minValue=-50, maxValue=50)  


    def process(self, image):
        """
        Adjusts the brightness of the given image based on the slider value.

        Args:
            image: The input image to be adjusted (e.g., a NumPy array or PIL Image).

        Returns:
            The brightness-adjusted image.
        """  
        # Get the current value of the slider
        value = self.slider.value()     

        # brighten the V channel of the HSVA image
        image[:, :, 2] = cv2.add(image[:, :, 2], value)

        return image

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        It also updates the label with the current value of the slider.
        """
        # Update the label with the current value
        self.label.setText(f"Brightness: {self.slider.value()}")
        
        super().on_change()



class ContrastBox(DraggableFunctionBox):
    """
    A box that allows the user to adjust the contrast of image.
    """
    def __init__(self, parent=None):
        super().__init__(CONTRAST_NAME, parent)

    def build_ui(self):
        
        # create a combo list to select between input type (range or T(s))
        self.combo = self.InsertComboList(["by Input-Output Range", "by T(s)"])

        # Create min and max input boxes for input range
        self.inMinMax = self.InsertMinMax("Input Range:")
        # Create min and max input boxes for output range
        self.outMinMax = self.InsertMinMax("Output Range:")

        # Create input boxes for alpha and beta values
        self.alpha = self.InsertSingleInput("Alpha:", defaultValue=1.0)
        self.beta = self.InsertSingleInput("Beta:", defaultValue=0.0)
        
        # hide the input range boxes by default
        for x in self.alpha + self.beta:
            x.hide()   
                    
    def process(self, image):
        """
        Adjusts the contrast of the given image based on the input and output range values.
        """
        if self.combo.currentText() == "by Input-Output Range":
            # get input and output range values from the text boxes
            in_min = int(self.inMinMax[0].text()) if self.inMinMax[0].text() else 0
            in_max = int(self.inMinMax[1].text()) if self.inMinMax[1].text() else 255
            out_min = int(self.outMinMax[0].text()) if self.outMinMax[0].text() else 0
            out_max = int(self.outMinMax[1].text()) if self.outMinMax[1].text() else 255

            # calculate the alpha and beta values
            alpha = (out_max - out_min) / (in_max - in_min)
            beta = out_min - (alpha * in_min)

            # return the contrast adjusted image
            return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)  

        elif self.combo.currentText() == "by T(s)":
            # get the alpha and beta values from input boxes
            alpha = float(self.alpha[0].text()) if self.alpha[0].text() and 0.0 < float(self.alpha[0].text()) <= 10.0 else 1.0
            beta = float(self.beta[0].text()) if self.beta[0].text() and -255 <= float(self.beta[0].text()) <= 255 else 0.0

            # return the contrast adjusted image
            return cv2.convertScaleAbs(image, -1, alpha, beta)

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """       
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
        super().__init__(FULL_SCALE_CONTRAST_NAME, parent)
  

    def process(self, image):
        """
        Performs full scale contrast stretching on the given image.
        This method adjusts the contrast of the image to span the full range of pixel values.
        """
        # return the contrast adjusted image
        return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)



class LogBox(DraggableFunctionBox):
    """
    A box that performs log transformation on the image.
    """
    def __init__(self, parent=None):
        super().__init__(LOG_NAME, parent)
  

    def process(self, image):
        """
        Performs log transformation on the given image.
        This method applies a logarithmic transformation to the image to enhance the contrast of dark regions.
        """
        image = image.astype(np.float32)    # convert image to float32 for log transformation
        image = np.log(1 + image)           # apply log transformation
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
        
        # convert image back to uint8 and return
        return image.astype(np.uint8)    



class GammaBox(DraggableFunctionBox):
    """
    A box that performs gamma transformation on the image.
    This is a non-linear transformation that can be used to adjust the brightness and contrast of the image.
    """
    def __init__(self, parent=None):
        super().__init__(GAMMA_NAME, parent)

  
    def build_ui(self):
        # insert signle input box for gamma value
        self.gamma = self.InsertSingleInput("Gamma:", defaultValue=1.0)


    def process(self, image):
        """
        Performs gamma transformation on the given image.
        This method applies a gamma transformation to the image to adjust the brightness and contrast.
        """
        # get the threshold value from input box
        gamma = float(self.gamma[0].text()) if self.gamma[0].text() and 0.0 < float(self.gamma[0].text()) <= 50.0 else 1.0
        
        image = image.astype(np.float32) / 255  # convert image to float32 for gamma transformation
        image = cv2.pow(image, gamma)           # apply gamma transformation
        
        # convert image back to uint8 and return
        return np.uint8(image * 255)     

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """       
        super().on_change()



class BlackAndWhiteBox(DraggableFunctionBox):
    """
    A box that converts image to black and white by thresholding.
    """
    def __init__(self, parent=None):
        super().__init__(BLACK_AND_WHITE_NAME, parent)

  
    def build_ui(self):
        # insert signle input box for threshold value
        self.threshold = self.InsertSingleInput("Threshold:", defaultValue=128)


    def process(self, image):
        """
        Converts the given image to black and white based on the threshold value.
        """
        # get the threshold value from input box
        threshold = int(self.threshold[0].text()) if self.threshold[0].text() and 0 <= int(self.threshold[0].text()) <= 255 else 128
        
        # convert image to black and white and return
        return cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)[1]

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """       
        super().on_change()



class ComplementBox(DraggableFunctionBox):
    """
    A box that performs complememnt of image.
    This is a simple image processing operation that inverts the colors of the image.
    """
    def __init__(self, parent=None):
        super().__init__(COMPLEMENT_NAME, parent)
  

    def process(self, image):
        """
        Performs complememnt of the given image.
        """
        # return the complememnt of image
        return cv2.bitwise_not(image)



class CropBox(DraggableFunctionBox):
    """
    A box that allows the user to crop the image.
    This class provides a UI for specifying the crop ranges and processes the image accordingly.
    """
    def __init__(self, parent=None):
        super().__init__(CROP_NAME, parent)

    def build_ui(self):
           
        # Create input boxes for crop ranges
        self.leftRight  = self.InsertMinMax("Left-Right:", 0, 0)      
        self.topBottom = self.InsertMinMax("Top-Bottom:", 0, 0)
                        

    def process(self, image):
        """
        Crops the given image based on the input range values.
        """
        lCut = int(self.leftRight[0].text()) if self.leftRight[0].text() else 0
        rCut = int(self.leftRight[1].text()) if self.leftRight[1].text() else 0
        tCut = int(self.topBottom[0].text()) if self.topBottom[0].text() else 0
        bCut = int(self.topBottom[1].text()) if self.topBottom[1].text() else 0

        return image[tCut:-1-bCut, lCut:-1-rCut]  

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """       
        super().on_change()



class FlipBox(DraggableFunctionBox):
    """
    A box that allows the user to flip the image.
    This class provides a UI for specifying the flip angle and processes the image accordingly.
    """
    def __init__(self, parent=None):
        super().__init__(FLIP_NAME, parent)

    def build_ui(self):
        # Create a radio button group to select the flip direction
        self.buttonGroup = self.InsertRadioButtons(["Horizontal", "Vertical", "Both"])

    def process(self, image):
        """
        Flips the given image based on the slider value.
        """    
        flipCodes = [1, 0, -1]                          # horizontal, vertical, both
        selectedId = self.buttonGroup.checkedId()       # get the selected radio button id

        # flip the image based on the selected id and return the result        
        return cv2.flip(image, flipCodes[selectedId])  

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """
        super().on_change()



class RotateBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(ROTATE_NAME, parent)

    def build_ui(self):
        # Create a slider to adjust the rotate angle
        self.slider, self.label = self.InsertSlider(heading="Angle: ", minValue=-180, maxValue=180)  


    def process(self, image):
        """
        Rotates the given image based on the slider value.
        This method rotates the image around its center by the specified angle.
        """        
        value = self.slider.value()         # Get the current value of the slider
        (h, w) = image.shape[:2]            # get the height and width of the image
        center = (w // 2, h // 2)           # rotate the center of the image
        M = cv2.getRotationMatrix2D(center, value, 1.0)  # get the rotation matrix
        
        # rotate the image using the rotation matrix and return the result
        return cv2.warpAffine(image, M, (w, h))

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        It also updates the label with the current value of the slider.
        """
        # Update the label with the current value
        self.label.setText(f"Angle: {self.slider.value()}")
        
        super().on_change()



class ResizeBox(DraggableFunctionBox):
    """
    A box that allows the user to resize the image.
    """
    def __init__(self, parent=None):
        super().__init__(RESIZE_NAME, parent)

    def build_ui(self):
        # Create min and max input boxes for input size
        self.newWidthHeight  = self.InsertMinMax("Size:", 0, 0)
        
        # set a flag to check if the input size is set to default values
        self.init = False
                        

    def process(self, image):
        """
        Resizes the given image based on the input size values.
        This method resizes the image to the specified width and height.
        """
        (w, h) = image.shape[:2]            # get the height and width of the image
        # set the default values for the input boxes
        if not self.init:
            self.newWidthHeight[0].setText(str(w))
            self.newWidthHeight[1].setText(str(h))
            self.init = True

        # get input and output range values from the text boxes
        reWidth = int(self.newWidthHeight[0].text()) if self.newWidthHeight[0].text() and int(self.newWidthHeight[0].text()) > 0 else w
        reHeight = int(self.newWidthHeight[1].text()) if self.newWidthHeight[1].text() and int(self.newWidthHeight[1].text()) > 0 else h

        # resize the image to the specified size and return the result
        return cv2.resize(image, (reWidth, reHeight))

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """       
        super().on_change()



class PaddingBox(DraggableFunctionBox):
    """
    A box that allows the user to add padding to the image.
    This class provides a UI for specifying the padding type and values.
    """
    def __init__(self, parent=None):
        super().__init__(PADDING_NAME, parent)

    def build_ui(self):
        # Create  a combo list to select the padding type
        self.combo = self.InsertComboList(["Constant", "Reflect", "Replicate"])

        # insert signle input box for constant value
        self.constant = self.InsertSingleInput("Value:", defaultValue=0)
        
        # Create input boxes for padding amounts
        self.leftRight = self.InsertMinMax("Left-Right:", 0, 0)      
        self.topBottom = self.InsertMinMax("Top-Bottom:", 0, 0)
                        

    def process(self, image):
        """
        Applies padding to the given image based on the selected padding type and values.
        This method adds padding to the image using the specified padding type and values.
        """
        # get the padding type based on the selected combo box value
        padCodes = [cv2.BORDER_CONSTANT, cv2.BORDER_REFLECT, cv2.BORDER_REPLICATE]
        selectedId = self.combo.currentIndex()        
        paddingType = padCodes[selectedId]

        # get the constant value from input box
        constant = int(self.constant[0].text()) if self.constant[0].text() and 0 <= int(self.constant[0].text()) <= 255 else 0

        # get the padding values from the input boxes
        lPad = int(self.leftRight[0].text()) if self.leftRight[0].text() else 0
        rPad = int(self.leftRight[1].text()) if self.leftRight[1].text() else 0
        tPad = int(self.topBottom[0].text()) if self.topBottom[0].text() else 0
        bPad = int(self.topBottom[1].text()) if self.topBottom[1].text() else 0

        if selectedId == 0:
            return cv2.copyMakeBorder(image, tPad, bPad, lPad, rPad, paddingType, value=constant)  # constant padding
        else:
            return cv2.copyMakeBorder(image, tPad, bPad, lPad, rPad, paddingType)   # reflect or replicate padding

    
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
        super().__init__(HISTEQ_NAME, parent)
  

    def process(self, image):
        """
        Performs histogram equalization on the given image.
        This method enhances the contrast of the image by redistributing the pixel intensity values.
        """
        # equalize the histogram of the given image and return the result
        return cv2.equalizeHist(image)



class HistCLAHEBox(DraggableFunctionBox):
    """
    CLAHE (Contrast Limited Adaptive Histogram Equalization) is a technique used to enhance the contrast of images.
    It is particularly useful for improving the visibility of details in images with varying lighting conditions.
    """
    def __init__(self, parent=None):
        super().__init__(HISTCLAHE_NAME, parent)

        # create input boxes for clip limit and tile grid size
        self.clipLimit = self.InsertSingleInput("Clip Limit:", defaultValue=2.0)
        self.tileGridSize = self.InsertSingleInput("Tile Grid Size:", defaultValue=8)

    def process(self, image):
        """
        Performs CLAHE on the given image.
        This method enhances the contrast of the image using the specified clip limit and tile grid size.
        """
        # get the clip limit and tile grid size values
        clipLimit = float(self.clipLimit[0].text()) if self.clipLimit[0].text() and 1.0 <= float(self.clipLimit[0].text()) <= 10.0 else 2.0
        tileGridSize = int(self.tileGridSize[0].text()) if self.tileGridSize[0].text() and 4 <= int(self.tileGridSize[0].text()) <= 64 else 8
        tileGridSize = tileGridSize if tileGridSize % 2 == 0 else 8        # allow only even numbers for tile grid size

        # create a CLAHE object with specified clip limit and tile grid size
        clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(tileGridSize, tileGridSize))

        # apply CLAHE to the image and return the result
        return clahe.apply(image)



class BitSliceBox(DraggableFunctionBox):
    """
    A box that allows the user to select a bit plane from the image.
    This class provides a UI for specifying the bit plane and processes the image accordingly.
    """
    def __init__(self, parent=None):
        super().__init__(BITSLICE_NAME, parent)

    def build_ui(self):
        # Create  a combo list to select a bit plane
        self.combo = self.InsertComboList(["0", "1", "2", "3", "4", "5", "6", "7"])
                        

    def process(self, image):
        """
        Extracts the selected bit plane from the given image.
        This method isolates the specified bit plane from the image and returns it as a binary image.
        """
        selectedId = self.combo.currentIndex()                  # get the padding type based on the selected combo box value
        image = cv2.bitwise_and(image, 1 << selectedId)         # get the selected bit plane
        image = np.where(image > 0, 255, 0).astype(np.uint8)    # convert the bit plane to binary image  

        return image

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """     
        super().on_change()



class NoiseBox(DraggableFunctionBox):
    """
    A box that allows the user to add noise to the image.
    This class provides a UI for specifying the noise type and parameters.
    """
    def __init__(self, parent=None):
        super().__init__(ADD_NOISE_NAME, parent)

    def build_ui(self):
        # Create  a combo list to select the noise type
        self.combo = self.InsertComboList(["Gaussian", "Salt & Pepper", "Poisson"])

        # insert signle input boxes for mean and std values
        self.mean = self.InsertSingleInput("Mean:", defaultValue=0)
        self.std = self.InsertSingleInput("Std.:", defaultValue=25.0)

        # insert signle input boxes for salt and pepper values
        self.saltProb = self.InsertSingleInput("Salt Prob.:", defaultValue=0.02)
        self.pepProb = self.InsertSingleInput("Pepper Prob.:", defaultValue=0.02)

        # hide the salt and pepper input boxes by default
        for x in self.saltProb + self.pepProb:
            x.hide()    

    def process(self, image):
        """
        Adds noise to the given image based on the selected noise type and parameters.
        This method applies the specified noise to the image and returns the noisy image.
        """
        if self.combo.currentText() == "Gaussian":
            # get mean and std values from the text boxes
            mean = float(self.mean[0].text()) if self.mean[0].text() and -100 <= float(self.mean[0].text()) <= 100 else 0.0
            std = float(self.std[0].text()) if self.std[0].text() and 0 <= float(self.std[0].text()) <= 100.0 else 25.0
            noise = np.random.normal(mean, std, image.shape)
            image = np.add(image, noise)  
            
            return np.clip(image, 0, 255).astype(np.uint8) 
        
        elif self.combo.currentText() == "Salt & Pepper":
            # get salt and pepper probability values from the text boxes
            saltProb = float(self.saltProb[0].text()) if self.saltProb[0].text() and 0 <= float(self.saltProb[0].text()) <= 1.0 else 0.02
            pepProb = float(self.pepProb[0].text()) if self.pepProb[0].text() and 0 <= float(self.pepProb[0].text()) <= 1.0 else 0.02

            numSalt = int(image.size * saltProb)       # number of salt pixels to add
            numPep = int(image.size * pepProb)         # number of pepper pixels to add

            saltCoords = [np.random.randint(0, i-1, numSalt) for i in image.shape]
            pepCoords = [np.random.randint(0, i-1, numPep) for i in image.shape]
            
            image[saltCoords[0], saltCoords[1]] = 255  # add salt noise
            image[pepCoords[0], pepCoords[1]] = 0      # add pepper noise

            return image
        
        elif self.combo.currentText() == "Poisson": 
            imageNoise = np.random.poisson(image)
            imageNoise = np.clip(imageNoise, 0, 255).astype(np.uint8)
            
            return imageNoise
    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """     

        if self.combo.currentText() == "Gaussian":
            # hide the salt and pepper input boxes and show the mean and std input boxes
            for x in self.mean + self.std:
                x.show()     
            for x in self.saltProb + self.pepProb:
                x.hide()

        elif self.combo.currentText() == "Salt & Pepper":
            # hide the mean and std input boxes and show the salt and pepper input boxes
            for x in self.saltProb + self.pepProb:
                x.show()
            for x in self.mean + self.std:
                x.hide()

        elif self.combo.currentText() == "Poisson": 
            # hide all the input boxes
            for x in self.saltProb + self.pepProb:
                x.hide()
            for x in self.mean + self.std:
                x.hide()

        super().on_change()



class RGB2GrayBox(DraggableFunctionBox):
    """
    A box that converts image from RGB to grayscale.
    This class provides a UI for specifying the conversion and processes the image accordingly.
    """
    def __init__(self, parent=None):
        super().__init__(RGB2GRAY_NAME, parent)
  

    def process(self, image):
        """
        Converts the given image from RGB to grayscale.
        This method transforms the image from RGB color space to grayscale.
        """
        totLayers = 1 if len(image.shape) == 2 else image.shape[2]          # get the number of layers in the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                      # convert the image to grayscale
        image = np.repeat(gray[:, :, np.newaxis], totLayers, axis=2)        # repeat the grayscale image to match the number of layers
        return image.astype(np.uint8)



class LaplaceBox(DraggableFunctionBox):
    """
    A box that performs laplace transformation on the image.
    """
    def __init__(self, parent=None):
        super().__init__(LAPLACE_NAME, parent)

  
    def build_ui(self):
        # insert switch for extended laplace choice
        self.norm = self.InsertSwitch("Normalize")
        
        # insert switch for extended laplace choice
        self.onOff = self.InsertSwitch("Extended Laplace")


    def process(self, image):
        """
        Performs laplace transformation on the given image.
        This method applies a laplace filter to the image to enhance the edges and details.
        """
        # normalize the image to 0-1 range
        image = image.astype(np.float32) / 255.0

        # create the laplace kernel
        if self.onOff.isChecked():
            w = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
        else:
            w = np.array([[0, 1, 0], [0, -4, 0], [0, 1, 0]], dtype=np.float32)

        # get the laplace filter
        laplace = cv2.filter2D(image, -1, w, borderType=cv2.BORDER_REPLICATE)
        
        # normalize the filtered image if the normalize switch is checked
        if self.norm.isChecked():
            laplace = cv2.normalize(laplace, None, 0, 1, cv2.NORM_MINMAX)
        
        # convert back to uint8 and return
        return (np.clip(laplace, 0, 1) * 255).astype(np.uint8)

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """       
        super().on_change()



class SobelBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(LAPLACE_NAME, parent)

  
    def build_ui(self):
        # insert switch for extended laplace choice
        self.norm = self.InsertSwitch("Normalize")
        

    def process(self, image):
        """
        """
        # normalize the image to 0-1 range
        image = image.astype(np.float32) / 255.0

        # create the sobel kernels
        w_x = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
        w_y = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)

        # get the sobel filters
        laplace_x = cv2.filter2D(image, -1, w_x, borderType=cv2.BORDER_REPLICATE)
        laplace_y = cv2.filter2D(image, -1, w_y, borderType=cv2.BORDER_REPLICATE)
        laplace = np.sqrt(laplace_x ** 2 + laplace_y ** 2)

        # normalize the filtered image if the normalize switch is checked
        if self.norm.isChecked():
            laplace = cv2.normalize(laplace, None, 0, 1, cv2.NORM_MINMAX)
        
        # convert back to uint8 and return
        return (np.clip(laplace, 0, 1) * 255).astype(np.uint8)

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """       
        super().on_change()



class SpatialFilterBox(DraggableFunctionBox):
    """
    A box that allows the user to apply spatial filters to the image.
    This class provides a UI for specifying the filter type and parameters.
    """
    def __init__(self, parent=None):
        super().__init__(SPATIAL_NAME, parent)

  
    def build_ui(self):
        # create a combo list to select spatial filter type
        self.combo = self.InsertComboList(["Median", "Max", "Min", "Mean", "Gaussian", "Laplace Sharpening", "Sobel Sharpening", "Unsharp Masking"])

        # insert a signle input box for kernel size
        self.kernel = self.InsertSingleInput("Kernel Size:", defaultValue=3)

        # insert a signle input box for sigma value
        self.sigma = self.InsertSingleInput("Std:", defaultValue=1.0)
        # hide the sigma input box by default
        for x in self.sigma:
            x.hide()

        # insert a signle input box for alpha value
        self.alpha = self.InsertSingleInput("Alpha:", defaultValue=1.0)
        # hide the alpha input box by default
        for x in self.alpha:
            x.hide()  

        # insert a switch for extended laplace choice
        self.extended = self.InsertSwitch("Extended Laplace")
        self.extended.hide()  # hide the switch by default

    def process(self, image):
        """
        Applies the selected spatial filter to the given image based on the specified parameters.
        This method processes the image using the selected filter type and parameters.
        """
        # get the kernel size from input box
        w = int(self.kernel[0].text()) if self.kernel[0].text() and int(self.kernel[0].text()) > 0 and int(self.kernel[0].text()) % 2 == 1 else 3
        # get the sigma value from input box
        sigma = float(self.sigma[0].text()) if self.sigma[0].text() and 0.0 < float(self.sigma[0].text()) <= 50.0 else 1.0
        # get the alpha value from input box
        alpha = float(self.alpha[0].text()) if self.alpha[0].text() and 0.0 < float(self.alpha[0].text()) <= 10.0 else 1.0
        # get the extended laplace choice from switch
        extended = self.extended.isChecked()

        if self.combo.currentText() == "Median":
            image = cv2.medianBlur(image, w)  # apply median filter

        elif self.combo.currentText() == "Max":
            image = cv2.dilate(image, np.ones((w, w), np.uint8), borderType=cv2.BORDER_REPLICATE)   # apply max filter

        elif self.combo.currentText() == "Min":
            image = cv2.erode(image, np.ones((w, w), np.uint8),borderType=cv2.BORDER_REPLICATE)     # apply min filter

        elif self.combo.currentText() == "Mean":
            image = cv2.blur(image, (w, w), borderType=cv2.BORDER_REPLICATE)    # apply mean filter

        elif self.combo.currentText() == "Gaussian":
            image = cv2.GaussianBlur(image, (w, w), sigma, borderType=cv2.BORDER_REPLICATE)  # apply gaussian filter
        
        elif self.combo.currentText() == "Laplace Sharpening":
            image = image.astype(np.float32) / 255    # normalize the image to 0-1 range
            
            # create the laplace kernel
            if extended:
                w = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
            else:
                w = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)
            
            laplace = cv2.filter2D(image, cv2.CV_32F, w, borderType=cv2.BORDER_REPLICATE)   # get the laplace filter
            image = image - laplace * alpha       # sharpen the image using the laplace filter

            image = np.clip(image, 0, 1)          # clip the image to 0-1 range
            image = (image * 255).astype(np.uint8)        # convert back to uint8

        elif self.combo.currentText() == "Sobel Sharpening":
            image = image.astype(np.float32) / 255.0    # normalize the image to 0-1 range

            # apply sobel kernel on x axis
            w_x = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
            laplace_x = cv2.filter2D(image, cv2.CV_32F, w_x, borderType=cv2.BORDER_REPLICATE)  # get the sobel filter on x axis
            image = image + laplace_x * alpha   # sharpen the image using the sobel filter

            # apply sobel kernel on y axis
            w_y = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
            laplace_y = cv2.filter2D(image, cv2.CV_32F, w_y, borderType=cv2.BORDER_REPLICATE)  # get the sobel filter on y axis
            image = image + laplace_y * alpha   # sharpen the image using the sobel filter

            image = np.clip(image, 0, 1) * 255    # clip the image to 0-1 range
            image = image.astype(np.uint8)        # convert back to uint8

        elif self.combo.currentText() == "Unsharp Masking":
            image = image.astype(np.float32) / 255.0    # normalize the image to 0-1 range
            imageBlurred = cv2.GaussianBlur(image, (w, w), sigma, borderType=cv2.BORDER_REPLICATE)     # get the blurred image
            imageSharp = image - imageBlurred       # get the sharpened filter
            image = image + imageSharp * alpha

            image = np.clip(image, 0, 1) * 255    # clip the image to 0-1 range
            image = image.astype(np.uint8)        # convert back to uint8

        return image

    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """    
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



class ArithmeticBox(DraggableFunctionBox):
    """
    """
    def __init__(self, parent=None):
        super().__init__(ARITHMETIC_NAME, parent)

        self.secondImage = None

  
    def build_ui(self):
        # insert a combo list to select the arithmetic operation
        self.combo = self.InsertComboList(["Add", "Subtract", "Multiply", "Divide"])
        
        # insert a signle input box for the alpha value
        self.alpha = self.InsertSingleInput("Alpha:", defaultValue=1.0)

        # insert a button to select the second image
        self.button = self.InsertButton("Select Image")
        self.button.clicked.connect(self.select_image)  # connect the button to the select_image function

    def process(self, image):
        """
        """
        if self.secondImage is None:
            return image

        # get the alpha value from input box
        alpha = float(self.alpha[0].text()) if self.alpha[0].text() and 0.0 < float(self.alpha[0].text()) <= 10.0 else 1.0

        self.secondImage = self.secondImage * alpha  # multiply the second image with alpha value

        # perform the selected arithmetic operation
        if self.combo == "Add":
            image = cv2.add(image, self.secondImage)
        elif self.combo == "Subtract":
            image = cv2.subtract(image, self.secondImage)
        elif self.combo == "Multiply":
            image = cv2.multiply(image, self.secondImage)
        elif self.combo == "Divide":
            image = cv2.divide(image, self.secondImage)

        return self.secondImage
    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """       
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
            self.secondImage = cv2.cvtColor(self.secondImage, cv2.COLOR_BGR2HSV)  # Convert the image to HSV color space
            self.secondImage = cv2.split(self.secondImage)[2]  # Extract the V channel from the HSV image

            self.on_change()        # emit the signal to indicate that the settings have been changed

