import numpy as np
import cv2

from PySide6.QtCore import Qt, Slot, Signal, QMimeData
from PySide6.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame, QSlider, 
                               QCheckBox, QComboBox, QLineEdit, QRadioButton, QButtonGroup, QFileDialog)
from PySide6.QtGui import QFont, QDrag


# function names
BRIGHTNESS_NAME = "Brightness"
SATURATION_NAME = "Saturation"
CONTRAST_NAME = "Contrast"
FULL_SCALE_CONTRAST_NAME = "Full Scale Contrast"
LOG_NAME = "Log Transform"
GAMMA_NAME = "Gamma Transform"
RGB2GRAY_NAME = "RGB to Gray"
THRESHOLDING_NAME = "Thresholding"
COMPLEMENT_NAME = "Complement"
CROP_NAME = "Crop"
FLIP_NAME = "Flip"
ROTATE_NAME = "Rotate"
RESIZE_NAME = "Resize"
PADDING_NAME = "Padding"
HISTEQ_NAME = "Histogram Equalization"
HISTCLAHE_NAME = "Local Hist. Equalization"
MASK_NAME = "Masking"
BITSLICE_NAME = "Bit Plane Slicing"
ADD_NOISE_NAME = "Add Noise"
ARITHMETIC_NAME = "Image Arithmetic"
LOGIC_NAME = "Image Logic"
LAPLACE_NAME = "Laplacian Filter"
SOBEL_NAME = "Sobel Filter"
SPATIAL_NAME = "Spatial Filter"

# list of function names to use in combo box
function_names = [BRIGHTNESS_NAME, SATURATION_NAME, CONTRAST_NAME, FULL_SCALE_CONTRAST_NAME, LOG_NAME, GAMMA_NAME, RGB2GRAY_NAME, 
                  THRESHOLDING_NAME, COMPLEMENT_NAME, CROP_NAME, FLIP_NAME, ROTATE_NAME, RESIZE_NAME, PADDING_NAME, HISTEQ_NAME,
                  HISTCLAHE_NAME, MASK_NAME, BITSLICE_NAME, ADD_NOISE_NAME, ARITHMETIC_NAME, LOGIC_NAME, LAPLACE_NAME, SOBEL_NAME, 
                  SPATIAL_NAME]


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
        label = QLabel(f"{heading}: {defaultValue}")
        label.setFont(self.font)
        self.contentLayout.addWidget(label, alignment=Qt.AlignLeft)

        # Create a slider to adjust brightness
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(minValue)
        slider.setMaximum(maxValue)
        slider.setValue(defaultValue)
        slider.valueChanged.connect(self.on_change)
        self.contentLayout.addWidget(slider)

        return [slider, label]


    def InsertMinMax(self, heading, defaultMin=0, defaultMax=255, minValue=0, maxValue=255):
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
    

    
    def InsertIntensityInput(self, heading, default1=0, default2=0, default3=0):
        """
        This function is called to insert min and max input boxes into the function box.
        """
        # Input range area
        layout1 = QHBoxLayout()
        layout1.setSpacing(0)
        self.contentLayout.addLayout(layout1)

        # an indicator for input range
        label = QLabel(heading)
        label.setFont(self.font)
        layout1.addWidget(label)

        # min value for input range 
        value1 = QLineEdit()
        value1.setFont(self.font)
        value1.setText(str(default1))
        value1.setFixedWidth(40)
        value1.textChanged.connect(self.on_change)
        layout1.addWidget(value1)

        # max value for input range
        value2 = QLineEdit()
        value2.setFont(self.font)
        value2.setText(str(default2))
        value2.setFixedWidth(40)
        value2.textChanged.connect(self.on_change)
        layout1.addWidget(value2)

        # max value for input range
        value3 = QLineEdit()
        value3.setFont(self.font)
        value3.setText(str(default3))
        value3.setFixedWidth(40)
        value3.textChanged.connect(self.on_change)
        layout1.addWidget(value3)

        return [value1, value2, value3, label]
    


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
        self.brightness = self.InsertSlider(heading="Brightness", minValue=-50, maxValue=50)  


    def process(self, imageHSVA):
        """
        Adjusts the brightness of the given image based on the slider value.

        Args:
            image: The input image to be adjusted (e.g., a NumPy array or PIL Image).

        Returns:
            The brightness-adjusted image.
        """  
        # Get the current value of the slider
        value = self.brightness[0].value()     

        # brighten the V channel of the HSVA image
        imageHSVA[:, :, 2] = cv2.add(imageHSVA[:, :, 2], value)

        return imageHSVA

    
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
        super().__init__(SATURATION_NAME, parent)

    def build_ui(self):
        # Create a slider to adjust saturation
        self.saturation = self.InsertSlider(heading="Saturation", minValue=-50, maxValue=50)


    def process(self, imageHSVA):
        """
        """  
        # Get the current value of the slider
        value = self.saturation[0].value()     

        imageBGR = cv2.cvtColor(imageHSVA[:, :, :3], cv2.COLOR_HSV2BGR)  # convert to BGR to check if image is grayscale 

        # saturate the S channel of the HSVA image if image is not grayscale
        if not (np.array_equal(imageBGR[:, :, 0], imageBGR[:, :, 1]) and np.array_equal(imageBGR[:, :, 1], imageBGR[:, :, 2])):
            imageHSVA[:, :, 1] = cv2.add(imageHSVA[:, :, 1], value)

        return imageHSVA

    
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
        super().__init__(CONTRAST_NAME, parent)

    def build_ui(self):
        
        # create a combo list to select between input type (range or T(s))
        self.combo = self.InsertComboList(["by Input-Output Range", "by T(s)"])

        # Create min and max input boxes for input range
        self.inMinMax = self.InsertMinMax("Input Range:")
        # Create min and max input boxes for output range
        self.outMinMax = self.InsertMinMax("Output Range:")

        # Create sliders for alpha and beta values
        self.alpha = self.InsertSlider(heading="Alpha:", minValue=1, maxValue=30, defaultValue=10)
        self.beta = self.InsertSlider(heading="Beta:", minValue=-50, maxValue=50)  
        
        # hide the input range boxes by default
        for x in self.alpha + self.beta:
            x.hide()   
                    
    def process(self, imageHSVA):
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

            # apply the contrast adjustment to the v channel of the HSVA image
            imageHSVA[:, :, 2] = cv2.convertScaleAbs(imageHSVA[:, :, 2], -1, alpha, beta) 

            return imageHSVA  

        elif self.combo.currentText() == "by T(s)":
            # get the alpha and beta values from sliders
            alpha = self.alpha[0].value()/10
            beta = self.beta[0].value()
            
            # apply the contrast adjustment to the v channel of the HSVA image
            imageHSVA[:, :, 2] = cv2.convertScaleAbs(imageHSVA[:, :, 2], -1, alpha, beta) 

            return imageHSVA

    
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
        super().__init__(FULL_SCALE_CONTRAST_NAME, parent)
  

    def process(self, imageHSVA):
        """
        Performs full scale contrast stretching on the given image.
        This method adjusts the contrast of the image to span the full range of pixel values.
        """
        # perform full scale contrast stretching
        imageHSVA[:, :, 2] = cv2.normalize(imageHSVA[:, :, 2], None, 0, 255, cv2.NORM_MINMAX)
        
        return imageHSVA



class LogBox(DraggableFunctionBox):
    """
    A box that performs log transformation on the image.
    """
    def __init__(self, parent=None):
        super().__init__(LOG_NAME, parent)
  

    def process(self, imageHSVA):
        """
        Performs log transformation on the given image.
        This method applies a logarithmic transformation to the image to enhance the contrast of dark regions.
        """
        vChannel = imageHSVA[:, :, 2]                 # get the V channel of the HSVA image

        vChannel = vChannel.astype(np.float32)    # convert the v channel to float32 for log transformation
        vChannel = np.log(1 + vChannel)           # apply log transformation
        vChannel = cv2.normalize(vChannel, None, 0, 255, cv2.NORM_MINMAX)
        
        imageHSVA[:, :, 2] = vChannel                 # update the V channel of the HSVA image

        return imageHSVA.astype(np.uint8)    



class GammaBox(DraggableFunctionBox):
    """
    A box that performs gamma transformation on the image.
    This is a non-linear transformation that can be used to adjust the brightness and contrast of the image.
    """
    def __init__(self, parent=None):
        super().__init__(GAMMA_NAME, parent)

  
    def build_ui(self):
        # insert signle input box for gamma value
        self.gamma = self.InsertSlider(heading="Gamma:", minValue=1, maxValue=100, defaultValue=10)


    def process(self, imageHSVA):
        """
        Performs gamma transformation on the given image.
        This method applies a gamma transformation to the image to adjust the brightness and contrast.
        """
        # get the threshold value from slider
        gamma = self.gamma[0].value()/10
        
        vChannel = imageHSVA[:, :, 2]                       # get the V channel of the HSVA image

        vChannel = vChannel.astype(np.float32) / 255    # convert the v channel to float32 for gamma transformation
        vChannel = cv2.pow(vChannel, gamma)             # apply gamma transformation
        
        imageHSVA[:, :, 2] = vChannel * 255                 # update the V channel of the HSVA image

        return np.uint8(imageHSVA)     

    
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
        super().__init__(RGB2GRAY_NAME, parent)
  

    def process(self, imageHSVA):
        """
        Converts the given image from RGB to grayscale.
        This method transforms the image from RGB color space to grayscale.
        """
        imageGray = imageHSVA[:, :, 2]                              # get only the v channel of the HSVA image
        imageBGR = cv2.cvtColor(imageGray, cv2.COLOR_GRAY2BGR)      # make the binary image 3 channel
        imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)        # convert back to HSV color space
        imageHSVA = cv2.merge((imageHSV, imageHSVA[:, :, 3]))       # set back the alpha channel of the image

        return imageHSVA



class ThresholdingBox(DraggableFunctionBox):
    """
    A box that converts image to black and white by thresholding.
    """
    def __init__(self, parent=None):
        super().__init__(THRESHOLDING_NAME, parent)

  
    def build_ui(self):
        # insert slider for threshold value
        self.threshold = self.InsertSlider(heading="Threshold:", minValue=0, maxValue=255, defaultValue=128)


    def process(self, imageHSVA):
        """
        Converts the given image to black and white based on the threshold value.
        """
        # get the threshold value from slider
        threshold = self.threshold[0].value()                                       

        imageGray = imageHSVA[:,:, 2]                # get only the v channel of the HSVA image
        imageBinary = cv2.threshold(imageGray, threshold, 255, cv2.THRESH_BINARY)[1]  # convert v channel to binary
        imageBGR = cv2.cvtColor(imageBinary, cv2.COLOR_GRAY2BGR)                      # make the binary image 3 channel
        imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)                          # convert back to HSV color space
        imageHSVA = cv2.merge((imageHSV, imageHSVA[:, :, 3]))                         # set back the alpha channel of the image 
        
        return imageHSVA


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
        super().__init__(COMPLEMENT_NAME, parent)
  

    def process(self, imageHSVA):
        """
        Performs complememnt of the given image.
        """
        imageBGR = cv2.cvtColor(imageHSVA[:, :, :3], cv2.COLOR_HSV2BGR)        # convert the HSVA image to BGR color space
        imageComplement = cv2.bitwise_not(imageBGR)                            # perform complememnt of the image
        imageHSV = cv2.cvtColor(imageComplement, cv2.COLOR_BGR2HSV)            # convert back to HSV color space
        imageHSVA = cv2.merge((imageHSV, imageHSVA[:, :, 3]))                  # set back the alpha channel of the image

        return imageHSVA



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
                        

    def process(self, imageHSVA):
        """
        Crops the given image based on the input range values.
        """
        leftCut = int(self.leftRight[0].text()) if self.leftRight[0].text() else 0
        rightCut = int(self.leftRight[1].text()) if self.leftRight[1].text() else 0
        topCut = int(self.topBottom[0].text()) if self.topBottom[0].text() else 0
        bottomCut = int(self.topBottom[1].text()) if self.topBottom[1].text() else 0

        return imageHSVA[topCut:-1-bottomCut, leftCut:-1-rightCut]  

    
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

    def process(self, imageHSVA):
        """
        Flips the given image based on the slider value.
        """    
        flipCodes = [1, 0, -1]                          # horizontal, vertical, both
        selectedId = self.buttonGroup.checkedId()       # get the selected radio button id

        # flip the image based on the selected id and return the result        
        return cv2.flip(imageHSVA, flipCodes[selectedId])  

    
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
        self.angle = self.InsertSlider(heading="Angle: ", minValue=-180, maxValue=180)  


    def process(self, imageHSVA):
        """
        Rotates the given image based on the slider value.
        This method rotates the image around its center by the specified angle.
        """        
        value = self.angle[0].value()         # Get the current value of the slider
        (h, w) = imageHSVA.shape[:2]            # get the height and width of the image
        center = (w // 2, h // 2)           # rotate the center of the image
        M = cv2.getRotationMatrix2D(center, value, 1.0)  # get the rotation matrix
        
        # rotate the image using the rotation matrix and return the result
        return cv2.warpAffine(imageHSVA, M, (w, h))

    
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
        super().__init__(RESIZE_NAME, parent)

    def build_ui(self):
        # Create min and max input boxes for input size
        self.newWidthHeight  = self.InsertMinMax("Size:", 0, 0)
        
        # set a flag to check if the input size is set to default values
        self.init = False
                        

    def process(self, imageHSVA):
        """
        Resizes the given image based on the input size values.
        This method resizes the image to the specified width and height.
        """
        (w, h) = imageHSVA.shape[:2]            # get the height and width of the image
        # set the default values for the input boxes
        if not self.init:
            self.newWidthHeight[0].setText(str(w))
            self.newWidthHeight[1].setText(str(h))
            self.init = True

        # get input and output range values from the text boxes
        reWidth = int(self.newWidthHeight[0].text()) if self.newWidthHeight[0].text() and int(self.newWidthHeight[0].text()) > 0 else w
        reHeight = int(self.newWidthHeight[1].text()) if self.newWidthHeight[1].text() and int(self.newWidthHeight[1].text()) > 0 else h

        # resize the image to the specified size and return the result
        return cv2.resize(imageHSVA, (reWidth, reHeight))

    
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
                        

    def process(self, imageHSVA):
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

        imageBGR = cv2.cvtColor(imageHSVA[:, :, :3], cv2.COLOR_HSV2BGR)  # convert the HSVA image to BGR color space

        if selectedId == 0:
            imageBGR = cv2.copyMakeBorder(imageBGR, tPad, bPad, lPad, rPad, paddingType, value=(constant, constant, constant))  # constant padding
            imageA = cv2.copyMakeBorder(imageHSVA[:, :, 3], tPad, bPad, lPad, rPad, paddingType, value=constant)  
        else:
            imageBGR = cv2.copyMakeBorder(imageBGR, tPad, bPad, lPad, rPad, paddingType)   # reflect or replicate padding
            imageA = cv2.copyMakeBorder(imageHSVA[:, :, 3], tPad, bPad, lPad, rPad, paddingType)   

        imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)    # convert back to HSV color space
        imageHSVA = cv2.merge((imageHSV, imageA))   # set back the alpha channel of the image

        return imageHSVA
    
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
  

    def process(self, imageHSVA):
        """
        Performs histogram equalization on the given image.
        This method enhances the contrast of the image by redistributing the pixel intensity values.
        """
        imageHSVA[:, :, 2] = cv2.equalizeHist(imageHSVA[:, :, 2])       # equalize the V channel of the HSVA image
        
        return imageHSVA
    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """    
        super().on_change()



class HistCLAHEBox(DraggableFunctionBox):
    """
    CLAHE (Contrast Limited Adaptive Histogram Equalization) is a technique used to enhance the contrast of images.
    It is particularly useful for improving the visibility of details in images with varying lighting conditions.
    """
    def __init__(self, parent=None):
        super().__init__(HISTCLAHE_NAME, parent)

    def build_ui(self):
        # create slider and input box for clip limit and tile grid size
        self.clipLimit = self.InsertSlider(heading="Clip Limit:", minValue=1, maxValue=100, defaultValue=2)  
        self.tileGridSize = self.InsertSingleInput("Tile Grid Size:", defaultValue=8)

    def process(self, imageHSVA):
        """
        Performs CLAHE on the given image.
        This method enhances the contrast of the image using the specified clip limit and tile grid size.
        """
        # get the clip limit and tile grid size values
        clipLimit = self.clipLimit[0].value()/10
        tileGridSize = int(self.tileGridSize[0].text()) if self.tileGridSize[0].text() and 4 <= int(self.tileGridSize[0].text()) <= 64 else 8
        tileGridSize = tileGridSize if tileGridSize % 2 == 0 else 8        # allow only even numbers for tile grid size

        # create a CLAHE object with specified clip limit and tile grid size
        clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(tileGridSize, tileGridSize))

        imageHSVA[:, :, 2] = clahe.apply(imageHSVA[:, :, 2])        # apply CLAHE to the V channel of the HSVA image

        return imageHSVA
    
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
        super().__init__(MASK_NAME, parent)

    def build_ui(self):
        # Create input boxes for mask range values
        self.intensityMin = self.InsertIntensityInput("min HSV:", 0, 0, 0)
        self.intensityMax = self.InsertIntensityInput("max HSV:", 0, 0, 0)

    def process(self, imageHSVA):
        """
        """
        # get the mask range values from the input boxes
        rMin = int(self.intensityMin[0].text()) if self.intensityMin[0].text() else 0
        gMin = int(self.intensityMin[0].text()) if self.intensityMin[0].text() else 0
        bMin = int(self.intensityMin[0].text()) if self.intensityMin[0].text() else 0
        rMax = int(self.intensityMax[1].text()) if self.intensityMax[1].text() else 0
        gMax = int(self.intensityMax[1].text()) if self.intensityMax[1].text() else 0
        bMax = int(self.intensityMax[1].text()) if self.intensityMax[1].text() else 0

        mask = cv2.inRange(imageHSVA[:, :, :3], np.array([rMin, gMin, bMin]), np.array([rMax, gMax, bMax]))   # create a mask based on the range values

        imageBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)            # convert the mask to BGR color space
        imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)                 # convert back to HSV color space
        imageHSVA = cv2.merge((imageHSV, imageHSVA[:, :, 3]))                # set back the alpha channel of the image

        return imageHSVA
    
    def on_change(self):
        """
        This function is called when the user changes the settings.
        It emits a signal to indicate that the settings have been changed.
        """   
        super().on_change()



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
                        

    def process(self, imageHSVA):
        """
        Extracts the selected bit plane from the given image.
        This method isolates the specified bit plane from the image and returns it as a binary image.
        """
        imageGray = cv2.bitwise_and(imageHSVA[:, :, 2], 1 << self.combo.currentIndex())         # get the selected bit plane
        imageBinary = np.where(imageGray > 0, 255, 0).astype(np.uint8)    # convert the bit plane to binary image  
        imageBGR = cv2.cvtColor(imageBinary, cv2.COLOR_GRAY2BGR)          # make the binary image 3 channel
        imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)              # convert back to HSV color space
        imageHSVA = cv2.merge((imageHSV, imageHSVA[:, :, 3]))             # set back the alpha channel of the image

        return imageHSVA

    
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
        # Create a combo list to select the noise type
        self.combo = self.InsertComboList(["Gaussian", "Salt & Pepper", "Poisson"])

        # insert signle input boxes for mean and std values
        self.mean = self.InsertSlider(heading="Mean:", minValue=-30, maxValue=300, defaultValue=0)
        self.std = self.InsertSlider(heading="Std:", minValue=0, maxValue=100, defaultValue=25)

        # insert signle input boxes for salt and pepper values
        self.saltPepProb = self.InsertSlider(heading="Probability:", minValue=0, maxValue=200, defaultValue=20)

        # hide the salt and pepper input boxes by default
        for x in self.saltPepProb:
            x.hide()    

    def process(self, imageHSVA):
        """
        Adds noise to the given image based on the selected noise type and parameters.
        This method applies the specified noise to the image and returns the noisy image.
        """
        if self.combo.currentText() == "Gaussian":
            # get mean and std values from the text boxes
            mean = self.mean[0].value() 
            std = self.std[0].value()
            
            imageBGR = cv2.cvtColor(imageHSVA[:, :, :3], cv2.COLOR_HSV2BGR)  # convert the HSVA image to BGR color space
            
            # If the image is grayscale, make the noise channels identical
            if np.array_equal(imageBGR[:, :, 0], imageBGR[:, :, 1]) and np.array_equal(imageBGR[:, :, 1], imageBGR[:, :, 2]):
                noise = np.random.normal(mean, std, imageBGR[:, :, 0].shape).astype(np.float32) 
                noise = cv2.merge((noise, noise, noise))
            else:
                noise = np.random.normal(mean, std, imageBGR.shape).astype(np.float32) 

            imageBGR = imageBGR.astype(np.float32) + noise              # add noise to the V channel of the HSVA image
            imageBGR = np.clip(imageBGR, 0, 255).astype(np.uint8)       # clip the values to the range [0, 255]
            imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)        # convert back to HSV color space
            imageHSVA = cv2.merge((imageHSV, imageHSVA[:, :, 3]))       # set back the alpha channel of the image
            
            return imageHSVA
        
        elif self.combo.currentText() == "Salt & Pepper":
            # get salt and pepper probability values from the text boxes
            saltPepProb = self.saltPepProb[0].value() / 1000

            numSalt = int(imageHSVA.size * saltPepProb)       # number of salt pixels to add
            numPep = int(imageHSVA.size * saltPepProb)         # number of pepper pixels to add

            saltCoords = [np.random.randint(0, i-1, numSalt) for i in imageHSVA.shape]
            pepCoords = [np.random.randint(0, i-1, numPep) for i in imageHSVA.shape]
            
            imageBGR = cv2.cvtColor(imageHSVA[:, :, :3], cv2.COLOR_HSV2BGR)  # convert the HSVA image to BGR color space

            imageBGR[saltCoords[0], saltCoords[1]] = [255, 255, 255]    # add salt noise
            imageBGR[pepCoords[0], pepCoords[1]] = [0,0,0]              # add pepper noise

            imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)        # convert back to HSV color space
            imageHSVA = cv2.merge((imageHSV, imageHSVA[:, :, 3]))       # set back the alpha channel of the image

            return imageHSVA.astype(np.uint8)       
        
        elif self.combo.currentText() == "Poisson": 
            imageBGR = cv2.cvtColor(imageHSVA[:, :, :3], cv2.COLOR_HSV2BGR)  # convert the HSVA image to BGR color space
            
            # If the image is grayscale, make the noise channels identical
            if np.array_equal(imageBGR[:, :, 0], imageBGR[:, :, 1]) and np.array_equal(imageBGR[:, :, 1], imageBGR[:, :, 2]):
                grayNoise = np.random.poisson(imageBGR[:, :, 0].astype(np.float32))
                imageBGR = cv2.merge((grayNoise, grayNoise, grayNoise))
            else:
                imageBGR = np.random.poisson(imageBGR.astype(np.float32))

            imageBGR = np.clip(imageBGR, 0, 255).astype(np.uint8)       
            imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)
            imageHSVA = cv2.merge((imageHSV, imageHSVA[:, :, 3]))
            
            return imageHSVA.astype(np.uint8)
    
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
        super().__init__(ARITHMETIC_NAME, parent)

        self.secondImage = None

  
    def build_ui(self):
        # insert a combo list to select the arithmetic operation
        self.combo = self.InsertComboList(["Add", "Subtract", "Multiply", "Divide"])
        
        # insert a slider for alpha value
        self.alpha = self.InsertSlider(heading="Alpha:", minValue=1, maxValue=1000, defaultValue=100)

        # insert a button to select the second image
        self.button = self.InsertButton("Select Image")
        self.button.clicked.connect(self.select_image)  # connect the button to the select_image function

    def process(self, imageHSVA):
        """
        """
        if self.secondImage is None:
            return imageHSVA
        
        alpha = self.alpha[0].value()/100           # get the alpha value from input box
        secondImage = (self.secondImage * alpha).astype(np.float32)  # multiply the second image with alpha value
        secondImage = cv2.resize(secondImage, (imageHSVA.shape[1], imageHSVA.shape[0]))  # resize the second image to match the size of the first image
        imageBGR = cv2.cvtColor(imageHSVA[:, :, :3], cv2.COLOR_HSV2BGR).astype(np.float32)  

        # perform the selected arithmetic operation
        if self.combo.currentText() == "Add":
            imageBGR = cv2.add(imageBGR, secondImage)
        elif self.combo.currentText() == "Subtract":
            imageBGR = cv2.subtract(imageBGR, secondImage)
        elif self.combo.currentText() == "Multiply":
            imageBGR = cv2.multiply(imageBGR, secondImage)
        elif self.combo.currentText() == "Divide":
            imageBGR = cv2.divide(imageBGR, secondImage + 1e-10)

        imageBGR = np.clip(imageBGR, 0, 255).astype(np.uint8)       # clip the values to the range [0, 255]
        imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)        # convert back to HSV color space
        imageHSVA = cv2.merge((imageHSV, imageHSVA[:, :, 3]))       # set back the alpha channel of the image

        return imageHSVA
    
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
        super().__init__(LOGIC_NAME, parent)

        self.secondImage = None

  
    def build_ui(self):
        # insert a combo list to select the logic operation
        self.combo = self.InsertComboList(["And", "Or", "Xor"])
        
        # insert a button to select the second image
        self.button = self.InsertButton("Select Image")
        self.button.clicked.connect(self.select_image)  # connect the button to the select_image function

    def process(self, imageHSVA):
        """
        """
        if self.secondImage is None:
            return imageHSVA
        
        # resize the second image to match the size of the first image
        secondImage = cv2.resize(self.secondImage, (imageHSVA.shape[1], imageHSVA.shape[0]))  
        imageBGR = cv2.cvtColor(imageHSVA[:, :, :3], cv2.COLOR_HSV2BGR)  

        # perform the selected arithmetic operation
        if self.combo.currentText() == "And":
            imageBGR = cv2.bitwise_and(imageBGR, secondImage)
        elif self.combo.currentText() == "Or":
            imageBGR = cv2.bitwise_or(imageBGR, secondImage)
        elif self.combo.currentText() == "Xor":
            imageBGR = cv2.bitwise_xor(imageBGR, secondImage)

        imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)        # convert back to HSV color space
        imageHSVA = cv2.merge((imageHSV, imageHSVA[:, :, 3]))       # set back the alpha channel of the image

        return imageHSVA.astype(np.uint8)       
    
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
        super().__init__(LAPLACE_NAME, parent)

  
    def build_ui(self):
        # insert switch for extended laplace choice
        self.norm = self.InsertSwitch("Normalize")
        
        # insert switch for extended laplace choice
        self.onOff = self.InsertSwitch("Extended Laplace")


    def process(self, imageHSVA):
        """
        Performs laplace transformation on the given image.
        This method applies a laplace filter to the image to enhance the edges and details.
        """
        vChannel = imageHSVA[:, :, 2]        # get the V channel of the HSVA image

        # normalize the v channel to 0-1 range
        vChannel = vChannel.astype(np.float32) / 255.0

        # create the laplace kernel
        if self.onOff.isChecked():
            w = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
        else:
            w = np.array([[0, 1, 0], [0, -4, 0], [0, 1, 0]], dtype=np.float32)

        # get the laplace filter
        laplace = cv2.filter2D(vChannel, -1, w, borderType=cv2.BORDER_REPLICATE)
        
        # normalize the filtered image if the normalize switch is checked
        if self.norm.isChecked():
            laplace = cv2.normalize(laplace, None, 0, 1, cv2.NORM_MINMAX)
        
        laplace = (np.clip(laplace, 0, 1) * 255).astype(np.uint8)
        imageBGR = cv2.merge((laplace, laplace, laplace))  
        imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)        # convert back to HSV color space
        imageHSVA = cv2.merge((imageHSV, imageHSVA[:, :, 3]))       # set back the alpha channel of the image
        return imageHSVA

    
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
        

    def process(self, imageHSVA):
        """
        """
        vChannel = imageHSVA[:, :, 2]        # get the V channel of the HSVA image
        vChannel = vChannel.astype(np.float32) / 255.0        # normalize the v channel to 0-1 range

        # create the sobel kernels
        w_x = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
        w_y = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)

        # get the sobel filters
        laplace_x = cv2.filter2D(vChannel, -1, w_x, borderType=cv2.BORDER_REPLICATE)
        laplace_y = cv2.filter2D(vChannel, -1, w_y, borderType=cv2.BORDER_REPLICATE)
        laplace = np.sqrt(laplace_x ** 2 + laplace_y ** 2)

        # normalize the filtered image if the normalize switch is checked
        if self.norm.isChecked():
            laplace = cv2.normalize(laplace, None, 0, 1, cv2.NORM_MINMAX)
        
        laplace = (np.clip(laplace, 0, 1) * 255).astype(np.uint8)
        imageBGR = cv2.merge((laplace, laplace, laplace))
        imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)        # convert back to HSV color space
        imageHSVA = cv2.merge((imageHSV, imageHSVA[:, :, 3]))       # set back the alpha channel of the image

        return imageHSVA

    
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

        # create a slider for sigma value
        self.sigma = self.InsertSlider(heading="Std:", minValue=0, maxValue=50, defaultValue=1)  
        # hide the sigma slider by default
        for x in self.sigma:
            x.hide()

        # insert a slider for alpha value
        self.alpha = self.InsertSlider(heading="Alpha:", minValue=1, maxValue=1000, defaultValue=100)
        # hide the alpha input box by default
        for x in self.alpha:
            x.hide()  

        # insert a switch for extended laplace choice
        self.extended = self.InsertSwitch("Extended Laplace")
        self.extended.hide()  # hide the switch by default

    def process(self, imageHSVA):
        """
        Applies the selected spatial filter to the given image based on the specified parameters.
        This method processes the image using the selected filter type and parameters.
        """
        # get the kernel size from input box
        w = int(self.kernel[0].text()) if self.kernel[0].text() and int(self.kernel[0].text()) > 0 and int(self.kernel[0].text()) % 2 == 1 else 3
        
        sigma = self.sigma[0].value()           # get the sigma value from input box
        alpha = self.alpha[0].value()/100       # get the alpha value from input box
        extended = self.extended.isChecked()    # get the extended laplace choice from switch

        vChannel = imageHSVA[:, :, 2]           # get the V channel of the HSVA image

        if self.combo.currentText() == "Median":
            vChannel = cv2.medianBlur(vChannel, w)  # apply median filter

        elif self.combo.currentText() == "Max":
            vChannel = cv2.dilate(vChannel, np.ones((w, w), np.uint8), borderType=cv2.BORDER_REPLICATE)   # apply max filter

        elif self.combo.currentText() == "Min":
            vChannel = cv2.erode(vChannel, np.ones((w, w), np.uint8),borderType=cv2.BORDER_REPLICATE)     # apply min filter

        elif self.combo.currentText() == "Mean":
            vChannel = cv2.blur(vChannel, (w, w), borderType=cv2.BORDER_REPLICATE)    # apply mean filter

        elif self.combo.currentText() == "Gaussian":
            vChannel = cv2.GaussianBlur(vChannel, (w, w), sigma, borderType=cv2.BORDER_REPLICATE)  # apply gaussian filter
        
        elif self.combo.currentText() == "Laplace Sharpening":
            vChannel = vChannel.astype(np.float32) / 255    # normalize the image to 0-1 range
            
            # create the laplace kernel
            if extended:
                w = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
            else:
                w = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)
            
            laplace = cv2.filter2D(vChannel, cv2.CV_32F, w, borderType=cv2.BORDER_REPLICATE)   # get the laplace filter
            vChannel = vChannel - laplace * alpha       # sharpen the image using the laplace filter

            vChannel = np.clip(vChannel, 0, 1)          # clip the image to 0-1 range
            vChannel = (vChannel * 255).astype(np.uint8)        # convert back to uint8

        elif self.combo.currentText() == "Sobel Sharpening":
            vChannel = vChannel.astype(np.float32) / 255.0    # normalize the image to 0-1 range

            # apply sobel kernel on x axis
            w_x = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
            laplace_x = cv2.filter2D(vChannel, cv2.CV_32F, w_x, borderType=cv2.BORDER_REPLICATE)  # get the sobel filter on x axis
            vChannel = vChannel + laplace_x * alpha   # sharpen the image using the sobel filter

            # apply sobel kernel on y axis
            w_y = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
            laplace_y = cv2.filter2D(vChannel, cv2.CV_32F, w_y, borderType=cv2.BORDER_REPLICATE)  # get the sobel filter on y axis
            vChannel = vChannel + laplace_y * alpha   # sharpen the image using the sobel filter

            vChannel = np.clip(vChannel, 0, 1) * 255    # clip the image to 0-1 range
            vChannel = vChannel.astype(np.uint8)        # convert back to uint8

        elif self.combo.currentText() == "Unsharp Masking":
            vChannel = vChannel.astype(np.float32) / 255.0    # normalize the image to 0-1 range
            Blurred = cv2.GaussianBlur(vChannel, (w, w), sigma, borderType=cv2.BORDER_REPLICATE)     # get the blurred image
            Sharp = vChannel - Blurred       # get the sharpened filter
            vChannel = vChannel + Sharp * alpha

            vChannel = np.clip(vChannel, 0, 1) * 255    # clip the image to 0-1 range
            vChannel = vChannel.astype(np.uint8)        # convert back to uint8

        if np.array_equal(imageHSVA[:, :, 0], imageHSVA[:, :, 1]) and np.array_equal(imageHSVA[:, :, 1], imageHSVA[:, :, 2]):
            imageBGR = cv2.merge((vChannel, vChannel, vChannel))  # make the image 3 channel
            imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)        # convert back to HSV color space
            imageHSVA = cv2.merge((imageHSV, imageHSVA[:, :, 3]))       # set back the alpha channel of the image
        else:
            imageHSVA[:, :, 2] = vChannel        # set the V channel of the HSVA image to the processed image

        return imageHSVA

    
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

