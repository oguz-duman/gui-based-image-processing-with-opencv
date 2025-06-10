import numpy as np
import cv2
import uuid

from PySide6.QtCore import Qt, Signal, QMimeData
from PySide6.QtGui import QFont, QDrag
from PySide6.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, 
                               QSizePolicy, QFrame, QCheckBox, QComboBox)

import constants
from gui.ui_management import UiManagement
from app.processors import Processors
from gui.ui_components import UiComponents 


class AddNewBox(QWidget):
    """
    A widget that allows the user to add new toolboxes.
    """
    # Signal to communicate with the main application
    trigger = Signal(str)

    def __init__(self):
        super().__init__()

        self.id = str(uuid.uuid4())                     # generate a unique id for the toolbox

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
        
        # Create a combo box to select the toolbox
        self.combo = QComboBox()
        self.combo.addItems([toolbox['NAME'] for toolbox in constants.TOOLBOXES.values()])
        self.combo.setFont(self.font)
        self.combo.setStyleSheet("padding: 5px;")  
        self.frameLayout.addWidget(self.combo, alignment=Qt.AlignVCenter)
        view = self.combo.view()
        view.setMouseTracking(False)  
        view.setAutoScroll(False)     
    
        # Create a button to add a new method
        newBtn = QPushButton("+")
        font = QFont()              
        font.setPointSize(20)  
        newBtn.setFont(font) 
        newBtn.setStyleSheet("padding-top: 5px; padding-bottom: 10px;")     
        newBtn.clicked.connect(lambda: self.trigger.emit(self.combo.currentText()))  
        self.frameLayout.addWidget(newBtn, alignment=Qt.AlignVCenter)



class Toolbox(QWidget, UiComponents, Processors):
    """
    A base class for all toolboxes. It provides a common interface.
    Parameters:
        title (str): The title of the toolbox.
    """
    # Signals to communicate with the main application
    updateTrigger = Signal()
    removeTrigger = Signal(str)
   

    def __init__(self, title="Toolbox"):
        super().__init__()

        self.contentLayout = QVBoxLayout()              # create a layout to hold the content of the toolbox

        self.set_parent(self.contentLayout)             # set the parent layout for the toolbox
        self.set_update_trigger(self.updateTrigger)     # set the update trigger for the toolbox

        self.title = title                      # set the title of the toolbox
        self.id = str(uuid.uuid4())             # generate a unique id for the toolbox
        self.initiate_ui()                      # set up the UI

    def initiate_ui(self):
        """
        Initiate the UI for the toolbox.
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

        # create a button to remove the toolbox
        removeBtn = QPushButton("X")
        removeBtn.setFont(self.font)
        removeBtn.setFixedWidth(30)
        removeBtn.clicked.connect(lambda: self.removeTrigger.emit(self.id))
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
    

    def update_toolbox(self, imageBGRA):
        """
        Runs only when the toolbox is created for the first time and everytime the input image is changed. 
        """
        self.imageBGRA = imageBGRA



class DraggableToolbox(Toolbox):
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



class BrightnessBox(DraggableToolbox):
    """
    A class to create a brightness adjustment toolbox.
    Adjusts the brightness of an image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['BRIGHTNESS']['NAME'])

        # Create a slider to adjust brightness
        self.brightness = self.insert_slider(heading="Brightness", minValue=-100, maxValue=100)  

    def execute(self, imageBGRA, mask):
        # apply brightness adjustment
        imageBGRA = self.adjust_brightness(imageBGRA, self.brightness[0].value(), mask)  

        return imageBGRA


class SaturationBox(DraggableToolbox):
    """
    A class to create a saturation adjustment toolbox.
    Adjusts the saturation of an image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['SATURATION']['NAME'])

        # Create a slider to adjust saturation
        self.saturation = self.insert_slider(heading="Saturation", minValue=-50, maxValue=50)

    def execute(self, imageBGRA, mask):
        # apply saturation adjustment
        imageBGRA = self.adjust_saturation(imageBGRA, self.saturation[0].value(), mask)     

        return imageBGRA


class ContrastBox(DraggableToolbox):
    """
    A class to create a contrast adjustment toolbox.
    Adjusts the contrast of an image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['CONTRAST']['NAME'])

        self.slider_rescale = 10    # set a rescale factor for the slider

        # insert a combo list to select between input type (range or T(s))
        self.combo = self.insert_combo_list(["by Input-Output Range", "by T(s)"])

        # insert min-max input boxes for input and output range
        self.inMinMax = self.insert_dual_input("Input Range:")
        self.outMinMax = self.insert_dual_input("Output Range:")

        # insert sliders for alpha and beta values
        self.alpha = self.insert_slider(heading="Alpha:", minValue=1, maxValue=30, defaultValue=10, rescale=self.slider_rescale)
        self.beta = self.insert_slider(heading="Beta:", minValue=-50, maxValue=50)  

        # connect widgets to the appropriate combo lists  
        self.set_combo_adapt_widgets(self.combo, [[self.inMinMax, self.outMinMax], [self.alpha, self.beta]])

    def execute(self, imageBGRA, mask):

        if self.combo.currentText() == "by Input-Output Range":
            # get input and output range values from the text boxes
            in_min, in_max = self.get_component_value(self.inMinMax[:2], maxs=[255,255], defaults=[0, 255])
            out_min, out_max = self.get_component_value(self.outMinMax[:2], maxs=[255,255], defaults=[0, 255])

            # apply contrast stretching using input-output range method
            imageBGRA = self.adjust_contrast_by_range(imageBGRA, [in_min, in_max], [out_min, out_max], mask)  

            return imageBGRA  

        elif self.combo.currentText() == "by T(s)":
            # get the alpha and beta values from sliders
            alpha = self.alpha[0].value() / self.slider_rescale
            beta = self.beta[0].value()

            # apply contrast stretching using T(s) method
            imageBGRA = self.adjust_contrast_by_T(imageBGRA, alpha, beta, mask)  
            
            return imageBGRA
              

class FullScaleContrastBox(DraggableToolbox):
    """
    A class to create a full scale contrast adjustment toolbox.
    Adjusts the contrast of an image to full scale.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['FULL_SCALE_CONTRAST']['NAME'])
  
    def execute(self, imageBGRA, mask):
        # apply full scale contrast stretching
        imageBGRA = self.apply_full_scale_contrast(imageBGRA, mask)  
        
        return imageBGRA


class LogBox(DraggableToolbox):
    """
    A class to create a log transformation toolbox.
    Applies a logarithmic transformation to an image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['LOG']['NAME'])
          
    def execute(self, imageBGRA, mask):
        # apply log transformation
        imageBGRA = self.apply_log_transform(imageBGRA, mask)  

        return imageBGRA


class GammaBox(DraggableToolbox):
    """
    A class to create a gamma transformation toolbox.
    Applies a gamma transformation to an image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['GAMMA']['NAME'])

        self.slider_rescale = 10        # set a rescale factor for the slider

        # insert signle input box to select the gamma value
        self.gamma = self.insert_slider(heading="Gamma:", minValue=1, maxValue=100, defaultValue=10, rescale=self.slider_rescale)

    def execute(self, imageBGRA, mask):
        gamma = self.gamma[0].value() / self.slider_rescale             # get the threshold value from slider
        imageBGRA = self.apply_gamma_transform(imageBGRA, gamma, mask)    # apply gamma transformation

        return np.uint8(imageBGRA)     


class RGB2GrayBox(DraggableToolbox):
    """
    A class to create a RGB to grayscale conversion toolbox.
    Converts the input image to grayscale.
    Works even if the input image is already grayscale.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['RGB2GRAY']['NAME'])

    def execute(self, imageBGRA, mask):
        # apply RGB to grayscale conversion
        imageBGRA = self.apply_rgb2gray_transform(imageBGRA)              

        return imageBGRA


class ThresholdingBox(DraggableToolbox):
    """
    A class to create a thresholding toolbox.
    Applies a thresholding operation to the input image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['THRESHOLDING']['NAME'])

        # insert slider to select the threshold value
        self.threshold = self.insert_slider(heading="Threshold:", minValue=0, maxValue=255, defaultValue=128)

    def execute(self, imageBGRA, mask):
        threshold = self.threshold[0].value()                               # get the threshold value from slider
        imageBGRA = self.apply_threshold_filter(imageBGRA, threshold)          # apply thresholding
        
        return imageBGRA


class ComplementBox(DraggableToolbox):
    """
    A class to create a complement toolbox.
    Applies a complement operation to the input image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['COMPLEMENT']['NAME'])
  
    def execute(self, imageBGRA, mask):
        imageBGRA = self.get_image_complement(imageBGRA)    # apply complement operation

        return imageBGRA


class CropBox(DraggableToolbox):
    """
    A class to create a cropping toolbox.
    Crops the input image based on the specified values.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['CROP']['NAME'])

        # Insert input boxes to select the crop values
        self.leftRight  = self.insert_dual_input("Left-Right:", 0, 0)      
        self.topBottom = self.insert_dual_input("Top-Bottom:", 0, 0)
                        
    def execute(self, imageBGRA, mask):
        h,w = imageBGRA.shape[:2]       # get the height and width of the input image

        # get the crop values from input
        leftCut, rightCut = self.get_component_value(self.leftRight[:2], maxs=[w,w], defaults=[0, 0])
        topCut, bottomCut = self.get_component_value(self.topBottom[:2], maxs=[h,h], defaults=[0, 0])
        
        # apply cropping
        imageBGRA = self.crop_image(imageBGRA, leftCut, rightCut, topCut, bottomCut)  

        return imageBGRA    


class FlipBox(DraggableToolbox):
    """
    A class to create a flipping toolbox.
    Flips the input image based on the selected direction.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['FLIP']['NAME'])

        # Insert a radio button group to select the flip direction
        self.buttonGroup = self.insert_radio_buttons(["Horizontal", "Vertical", "Both"])

    def execute(self, imageBGRA, mask):
        flipCodes = [1, 0, -1]          # horizontal, vertical, both
        imageBGRA = self.flip_image(imageBGRA, flipCodes[self.buttonGroup[0].checkedId()])  # apply flipping

        return imageBGRA
    

class RotateBox(DraggableToolbox):
    """
    A class to create a rotation toolbox.
    Rotates the input image based on the selected angle.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['ROTATE']['NAME'])

        # Insert a slider to adjust the rotate angle
        self.angle = self.insert_slider(heading="Angle: ", minValue=-180, maxValue=180)  

    def execute(self, imageBGRA, mask):
        value = self.angle[0].value()                           # Get the current value of the slider
        imageBGRA = self.rotate_image(imageBGRA, value)         # Apply rotation

        return imageBGRA


class ResizeBox(DraggableToolbox):
    """
    A class to create a resizing toolbox.
    Resizes the input image based on the specified width and height.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['RESIZE']['NAME'])

        self.im_width = 0
        self.im_height = 0
                        
    def execute(self, imageBGRA, mask):

        if self.combo.currentText() == "Resize by Absolute Size":
            # get input and output range values from the text boxes
            reWidth, reHeight = self.get_component_value(self.newWidthHeight[:2], mins=[0, 0], defaults=[self.im_width, self.im_height])
        elif self.combo.currentText() == "Resize by Percentage":
            # get the percentage value from the slider and calculate the new width and height
            percentage = self.percentage[0].value() / 100
            reWidth = int(self.im_width * percentage)
            reHeight = int(self.im_height * percentage)
            
        # apply resizing
        imageBGRA = self.resize_image(imageBGRA, reWidth, reHeight, self.interpolation_types[self.interpolation.currentIndex()])  
    
        return imageBGRA


    def update_toolbox(self, imageBGRA):
        """
        Runs only when the toolbox is created for the first time and everytime the input image is changed. 
        """
        super().update_toolbox(imageBGRA)

        if [self.im_width, self.im_height] == [0, 0]:
            
            # insert a combo list to select between resize by absolute size and by percentage
            self.combo = self.insert_combo_list(["Resize by Absolute Size", "Resize by Percentage"])

            # insert a slider to select the percentage value
            self.percentage = self.insert_slider(heading="Percentage:", minValue=1, maxValue=100, defaultValue=100)

            # Insert min-max input boxes to select the new size
            self.newWidthHeight  = self.insert_dual_input("Size:", 0, 0)

            # order of the interpolation types in this list must be in the same order as in self.interpolation_types
            self.interpolation = self.insert_combo_list(["None", "INTER_NEAREST", "INTER_LINEAR", "INTER_AREA", "INTER_CUBIC",
                                                        "INTER_LANCZOS4", "INTER_LINEAR_EXACT"])
            
            self.interpolation_types = [None, cv2.INTER_NEAREST, cv2.INTER_LINEAR, cv2.INTER_AREA, cv2.INTER_CUBIC,
                                        cv2.INTER_LANCZOS4, cv2.INTER_LINEAR_EXACT]
            
            # connect widgets to the appropriate combo lists
            self.set_combo_adapt_widgets(self.combo, [[self.newWidthHeight], [self.percentage]])
            
            # get the height and width of the image
            self.im_width, self.im_height = [128, 128] if self.imageBGRA is None else self.imageBGRA.shape[:2]  

            # set the input boxes to the image size as default
            self.newWidthHeight[0].setText(str(self.im_height))
            self.newWidthHeight[1].setText(str(self.im_width))
                 

class PaddingBox(DraggableToolbox):
    """
    A class to create a padding toolbox.
    Applies padding to the input image based on the selected type and values.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['PADDING']['NAME'])

        # Insert a combo list to select the padding type
        self.combo = self.insert_combo_list(["Constant", "Reflect", "Replicate"])

        # Insert a signle input box to select the constant value
        self.constant = self.insert_mono_input("Value:", defaultValue=0)
        
        # Insert input boxes to select the padding values
        self.leftRight = self.insert_dual_input("Left-Right:", 0, 0)      
        self.topBottom = self.insert_dual_input("Top-Bottom:", 0, 0)

         # connect widgets to the appropriate combo lists 
        self.set_combo_adapt_widgets(self.combo, [[self.constant, self.leftRight, self.topBottom], 
                                                                [self.leftRight, self.topBottom], [self.leftRight, self.topBottom]])

    def execute(self, imageBGRA, mask):
        # get the padding type based on the selected combo box value
        padCodes = [cv2.BORDER_CONSTANT, cv2.BORDER_REFLECT, cv2.BORDER_REPLICATE]
        selectedId = self.combo.currentIndex()        
        paddingType = padCodes[selectedId]

        # get the input values from the input boxes
        constant = self.get_component_value(self.constant[:1], mins=[0], maxs=[255], defaults=[0])
        lPad, rPad = self.get_component_value(self.leftRight[:2], defaults=[0, 0])
        tPad, bPad = self.get_component_value(self.topBottom[:2], defaults=[0, 0])

        # apply padding
        imageBGRA = self.apply_padding(imageBGRA, paddingType, lPad, rPad, tPad, bPad, constant)  

        return imageBGRA


class HistEqualizationBox(DraggableToolbox):
    """
    A class to create a histogram equalization toolbox.
    Applies histogram equalization to the input image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['HISTEQ']['NAME'])
  
    def execute(self, imageBGRA, mask):
        # apply histogram equalization
        imageBGRA = self.apply_histogram_equalization(imageBGRA, mask)  
        
        return imageBGRA


class HistCLAHEBox(DraggableToolbox):
    """
    A class to create a histogram CLAHE toolbox.
    Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) to the input image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['HISTCLAHE']['NAME'])

        self.clipLimit_rescale = 10     # set a rescale factor for the slider

        # Insert a slider and input box to select the clip limit and tile grid size
        self.clipLimit = self.insert_slider(heading="Clip Limit:", minValue=1, maxValue=100, defaultValue=2, rescale=self.clipLimit_rescale)  
        self.tileGridSize = self.insert_mono_input("Tile Grid Size:", defaultValue=8)

    def execute(self, imageBGRA, mask):
        # get the clip limit and tile grid size values
        clipLimit = self.clipLimit[0].value() / self.clipLimit_rescale
        tileGridSize = self.get_component_value(self.tileGridSize[:1], mins=[4], maxs=[64], defaults=[8])
        tileGridSize = tileGridSize if tileGridSize % 2 == 0 else tileGridSize + 1          # allow only even numbers for tile grid size

        # apply CLAHE
        imageBGRA = self.apply_clahe(imageBGRA, clipLimit, tileGridSize, mask)

        return imageBGRA
    

class ColorMaskBox(DraggableToolbox):
    """
    A class to create a masking toolbox.
    This toolbox allows the user to select a range of HSV values to create a mask.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['COLOR_MASKING']['NAME'])

        # Insert a switch to invert the mask
        self.invert = self.insert_switch("Invert the mask")

        # Insert input boxes to select the min-max HSV values
        self.intensityMin = self.insert_triple_input("min HSV:", 0, 0, 0)
        self.intensityMax = self.insert_triple_input("max HSV:", 0, 0, 0)

    def execute(self, imageBGRA, mask):
        # get the min-max HSV values from the input boxes
        rMin, gMin, bMin = self.get_component_value(self.intensityMin[:3], mins=[0, 0, 0], maxs=[255,255, 255], defaults=[0, 0, 0])
        rMax, gMax, bMax = self.get_component_value(self.intensityMax[:3], mins=[0, 0, 0], maxs=[255,255, 255], defaults=[0, 0, 0])

        # apply masking
        mask = self.generate_color_mask(imageBGRA, np.asarray([rMin, gMin, bMin]), np.asarray([rMax, gMax, bMax]), self.invert[0].isChecked())

        return imageBGRA, mask
    

class SpatialMaskBox(DraggableToolbox):
    """
    A class to create a masking toolbox.
    This toolbox allows the user to select a rectangular area of the image and apply spatial masking.
    This mask only affects the next toolbox in the pipeline not all 
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['SPATIAL_MASKING']['NAME'])

        self.im_size = [0, 0]


    def execute(self, imageBGRA, mask):

        # get the slider values and apply spatial masking
        mask = self.generate_spatial_mask(imageBGRA, self.slid_width[0].value(), self.slid_height[0].value(),
                                                    self.slid_left[0].value(), self.slid_top[0].value(), 
                                                    self.slid_bor_radius[0].value(), self.invert[0].isChecked()) 

        return imageBGRA, mask
    
    
    def update_toolbox(self, imageBGRA):
        super().update_toolbox(imageBGRA)  

        if self.im_size == [0, 0]:
        
            # get the height and width of the image
            self.im_size = [0, 0] if self.imageBGRA is None else self.imageBGRA.shape[:2]  

            # insert a switch to invert the mask
            self.invert = self.insert_switch("Invert the mask")
            
            # insert sliders for width, height, left position, top position and border radius
            self.slid_width = self.insert_slider(heading="Width:", minValue=1, maxValue=self.im_size[1], defaultValue=self.im_size[1])
            self.slid_height = self.insert_slider(heading="Height:", minValue=1, maxValue=self.im_size[0], defaultValue=self.im_size[0])
            self.slid_left = self.insert_slider(heading="Left:", minValue=0, maxValue=self.im_size[1], defaultValue=0)
            self.slid_top = self.insert_slider(heading="Top:", minValue=0, maxValue=self.im_size[0], defaultValue=0)
            self.slid_bor_radius = self.insert_slider(heading="Border Radius:", minValue=0, maxValue=100, defaultValue=0) 
        

class BitSliceBox(DraggableToolbox):
    """
    A class to create a bit plane slicing toolbox.
    Applies bit plane slicing to the input image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['BITSLICE']['NAME'])

        # Insert a combo list to select a bit plane
        self.combo = self.insert_combo_list(["0", "1", "2", "3", "4", "5", "6", "7"])

    def execute(self, imageBGRA, mask):
        # apply bit plane slicing
        imageBGRA = self.extract_bit_planes(imageBGRA, int(self.combo.currentText()))

        return imageBGRA


class NoiseBox(DraggableToolbox):
    """
    A class to create a noise toolbox.
    Applies different types of noises to the input image.
    Available noise types are Gaussian, Salt & Pepper, and Poisson.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['ADD_NOISE']['NAME'])

        self.saltPepProb_rescale = 1000         # set a rescale factor for the slider

        # Insert a combo list to select the noise type
        self.combo = self.insert_combo_list(["Gaussian", "Salt & Pepper", "Poisson"])

        # insert signle input boxes to select the mean and std values
        self.mean = self.insert_slider(heading="Mean:", minValue=-30, maxValue=300, defaultValue=0)
        self.std = self.insert_slider(heading="Std:", minValue=0, maxValue=100, defaultValue=25)

        # insert signle input boxes to select the salt and pepper probability
        self.saltPepProb = self.insert_slider(heading="Probability:", minValue=0, maxValue=200, defaultValue=20, rescale=self.saltPepProb_rescale)

         # connect widgets to the appropriate combo lists 
        self.set_combo_adapt_widgets(self.combo, [[self.mean, self.std], [self.saltPepProb], []])
   
    def execute(self, imageBGRA, mask):
        if self.combo.currentText() == "Gaussian":
            # get mean and std values from inputs and apply gaussian noise
            mean = self.mean[0].value() 
            std = self.std[0].value()
            imageBGRA = self.add_gaussian_noise(imageBGRA, mean, std, mask)  
            
            return imageBGRA
        
        elif self.combo.currentText() == "Salt & Pepper":
            # get salt and pepper probability values from the text boxes and apply salt and pepper noise
            saltPepProb = self.saltPepProb[0].value() / self.saltPepProb_rescale
            imageBGRA = self.add_salt_and_pepper(imageBGRA, saltPepProb, mask)
            
            return imageBGRA    
        
        elif self.combo.currentText() == "Poisson": 
            # apply poisson noise
            imageBGRA = self.add_poisson_noise(imageBGRA, mask)
            
            return imageBGRA
   

class ArithmeticBox(DraggableToolbox):
    """
    A class to create an arithmetic operation toolbox.
    Applies arithmetic operations with the input image and a selected second image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['ARITHMETIC']['NAME'])

        self.secondImage = None         # set a variable to store the second image
        self.alpha_rescale = 100        # set a rescale factor for the slider

        # insert a combo list to select the arithmetic operation
        self.combo = self.insert_combo_list(["Add", "Subtract", "Multiply", "Divide"])
        
        # insert a slider to select the alpha value
        self.alpha = self.insert_slider(heading="Alpha:", minValue=1, maxValue=1000, defaultValue=100, rescale=self.alpha_rescale)

        # insert a button to select a new second image
        self.button = self.insert_button("Select Image")
        self.button[0].clicked.connect(self.open_second_image_button)  # connect the button click to the open_second_image_button method

    def execute(self, imageBGRA, mask):
        if self.secondImage is not None:
            alpha = self.alpha[0].value() / self.alpha_rescale                      # get the alpha value from input 
            operation = self.combo.currentText()                                    # get the selected operation from combo box
            imageBGRA = self.apply_image_arithmetic(imageBGRA, self.secondImage, alpha, operation)  # apply arithmetic operation

        return imageBGRA
    
    def open_second_image_button(self):
        """
        Open a file dialog to select the second image.
        """
        imageBGRA = UiManagement.select_image(None)     # read the image

        if imageBGRA is not None:
            self.secondImage = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)  # convert the image to BGR format
            self.updateTrigger.emit()        # emit the signal to indicate that the settings have been changed


class LogicBox(DraggableToolbox):
    """
    A class to create a logic operation toolbox.
    Applies logic operations with the input image and a selected second image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['LOGIC']['NAME'])


        self.secondImage = None         # set a variable to store the second image

        # insert a combo list to select the logic operation
        self.combo = self.insert_combo_list(["And", "Or", "Xor"])
        
        # insert a button to select the second image
        self.button = self.insert_button("Select Image")
        self.button[0].clicked.connect(self.open_second_image_button)  # connect the button click to the open_second_image_button method


    def execute(self, imageBGRA, mask):
        if self.secondImage is not None:
            operation = self.combo.currentText()                                        # get the selected operation from combo box
            imageBGRA = self.perform_image_logic(imageBGRA, self.secondImage, operation)    # apply logic operation

        return imageBGRA 

    def open_second_image_button(self):
        """
        Open a file dialog to select the second image.
        """
        imageBGRA = UiManagement.select_image(None)     # read the image

        if imageBGRA is not None:
            self.secondImage = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)  # convert the image to BGR format
            self.updateTrigger.emit()        # emit the signal to indicate that the settings have been changed


class LaplaceBox(DraggableToolbox):
    """
    A class to create a laplace transformation toolbox.
    Applies a laplace transformation to the input image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['LAPLACE']['NAME'])


        # insert switch to select extended laplace and normalize options
        self.extended = self.insert_switch("Extended Laplace")
        self.norm = self.insert_switch("Normalize")

    def execute(self, imageBGRA, mask):
        # apply laplace transformation
        imageBGRA = self.get_laplacian_filter(imageBGRA, self.extended[0].isChecked(), self.norm[0].isChecked())  

        return imageBGRA


class SobelBox(DraggableToolbox):
    """
    A class to create a sobel transformation toolbox.
    Applies a sobel transformation to the input image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['SOBEL']['NAME'])

        # insert a switch to select the normalize option
        self.norm = self.insert_switch("Normalize")
        
    def execute(self, imageBGRA, mask):
        # apply sobel transformation
        imageBGRA = self.get_sobel_filter(imageBGRA, self.norm[0].isChecked())  

        return imageBGRA


class OrderStatBox(DraggableToolbox):
    """
    A class to create an order statistics toolbox.
    Applies order statistics filtering to the input image.
    Available methods are Median, Max, and Min.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['ORDER_STAT']['NAME'])

        # insert nedded input widgets
        self.combo = self.insert_combo_list(["Median", "Max", "Min"])
        self.kernel = self.insert_mono_input("Kernel Size:", defaultValue=3)

         # connect widgets to the appropriate combo lists 
        self.set_combo_adapt_widgets(self.combo, [[self.kernel], [self.kernel], [self.kernel]])

    def execute(self, imageBGRA, mask):
        # get the kernel size and make sure it is odd
        w = self.get_component_value(self.kernel[:1], mins=[0], defaults=[3])         
        w = w if w % 2 == 1 else w + 1                                      
        
        # apply the selected smoothing method
        if self.combo.currentText() == "Median":
            imageBGRA = self.apply_order_stat_filter(imageBGRA, w, "median", mask)  
        elif self.combo.currentText() == "Max":
            imageBGRA = self.apply_order_stat_filter(imageBGRA, w, "max", mask)  
        elif self.combo.currentText() == "Min":
            imageBGRA = self.apply_order_stat_filter(imageBGRA, w, "min", mask)   

        return imageBGRA


class SmoothingBox(DraggableToolbox):
    """
    A class to create a smoothing toolbox.
    Applies smoothing to the input image.
    Available methods are Mean and Gaussian.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['SMOOTHING']['NAME'])

        # set rescale factor for sigma slider
        self.sigma_rescale = 10

        # insert nedded input widgets
        self.combo = self.insert_combo_list(["Mean", "Gaussian"])
        self.kernel = self.insert_mono_input("Kernel Size:", defaultValue=3)
        self.sigma = self.insert_slider(heading="Std:", minValue=1, maxValue=100, defaultValue=10, rescale=self.sigma_rescale)  

         # connect widgets to the appropriate combo lists 
        self.set_combo_adapt_widgets(self.combo, [[self.kernel], [self.kernel, self.sigma]])

    def execute(self, imageBGRA, mask):
        # get the kernel size and make sure it is odd
        w = self.get_component_value(self.kernel[:1], mins=[0], defaults=[3])         
        w = w if w % 2 == 1 else w + 1                                      
        
        # get the sigma value from inputs
        sigma = self.sigma[0].value() / self.sigma_rescale      
        
        # apply the selected smoothing method
        if self.combo.currentText() == "Mean":
            imageBGRA = self.apply_box_filter(imageBGRA, w, mask)
        elif self.combo.currentText() == "Gaussian":
            imageBGRA = self.apply_gaussian_blur(imageBGRA, w, sigma, mask)  

        return imageBGRA
    

class SharpeningBox(DraggableToolbox):
    """
    A class to create a sharpening toolbox.
    Applies sharpening to the input image.
    Available methods are Laplace, Sobel, and Unsharp Masking.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['SHARPENING']['NAME'])

        # set rescale factors for sliders
        self.alpha_rescale = 100
        self.sigma_rescale = 10

        # insert nedded input widgets
        self.combo = self.insert_combo_list(["Laplace Sharpening", "Sobel Sharpening", "Unsharp Masking"])
        self.kernel = self.insert_mono_input("Kernel Size:", defaultValue=3)
        self.sigma = self.insert_slider(heading="Std:", minValue=1, maxValue=100, defaultValue=10, rescale=self.sigma_rescale)  
        self.extended = self.insert_switch("Extended Laplace")
        self.alpha = self.insert_slider(heading="Alpha:", minValue=1, maxValue=1000, defaultValue=100, rescale=self.alpha_rescale)

         # connect widgets to the appropriate combo lists 
        self.set_combo_adapt_widgets(self.combo, [[self.extended, self.alpha], [self.alpha],
                                                                 [self.kernel, self.sigma, self.alpha]])

    def execute(self, imageBGRA, mask):
        # get the kernel size and make sure it is odd
        w = self.get_component_value(self.kernel[:1], mins=[0], defaults=[3])         
        w = w if w % 2 == 1 else w + 1                                      
        
        # get the sigma, alpha and extended laplace values from inputs
        sigma = self.sigma[0].value() / self.sigma_rescale      
        alpha = self.alpha[0].value() / self.alpha_rescale      
        extended = self.extended[0].isChecked()                 
        
        # apply the selected sharpening method
        if self.combo.currentText() == "Laplace Sharpening":
            imageBGRA = self.apply_laplacian_sharpening(imageBGRA, alpha, extended, mask)
        elif self.combo.currentText() == "Sobel Sharpening":
            imageBGRA = self.apply_sobel_sharpening(imageBGRA, alpha, mask)
        elif self.combo.currentText() == "Unsharp Masking":
            imageBGRA = self.apply_unsharp_mask(imageBGRA, w, sigma, alpha, mask)

        return imageBGRA
    

class FrequencyFilterBox(DraggableToolbox):
    """
    A class to create a frequency domain filtering toolbox.
    Applies low-pass or high-pass filtering to the input image in the frequency domain.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['FREQ_FILTER']['NAME'])

        # insert a combo list to select the filter type
        self.combo = self.insert_combo_list(["Low Pass", "High Pass"])
        
        # insert a slider to select the filter radius
        self.filter_radius = self.insert_slider(heading="Filter Radius:", minValue=1, maxValue=200, defaultValue=30)
        

    def execute(self, imageBGRA, mask):

        filter_radius = self.filter_radius[0].value()          # get the first filter radius value
        filter_type = self.combo.currentText()                   # get the selected filter type from combo box
        
        # apply the selected frequency filter
        imageBGRA = self.apply_frequency_filter(imageBGRA, filter_radius, filter_type)

        return imageBGRA