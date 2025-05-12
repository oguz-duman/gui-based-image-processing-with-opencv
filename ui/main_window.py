import cv2
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import traceback

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap, QFont, QImage
from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QScrollArea,
    QFileDialog, QMessageBox
)

# Import custom function boxes
from constants import CHANNEL_NAMES
from processing.pipeline import Pipeline
from ui import toolboxes
import constants
import utils


# -------------------------- main class definitions -------------------

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()  

        self.init_variables()  # Initialize variables
        self.init_ui()      # Initialize UI
        

    def init_ui(self):
        """
        Initialize the UI components and layout.
        """
        # Create main layout and set it to the widget
        self.mainLayout = QVBoxLayout(self) 
        self.mainLayout.setContentsMargins(20, 5, 20, 5) 
        self.mainLayout.setSpacing(15)

        # init top, mid and bottom layouts
        self.init_topLayout()
        self.init_midLayout()
        self.init_bottomLayout()


    def init_variables(self):
        """
        Initialize the variables used in the widget.
        """
        self.pipeline = Pipeline()  # create an instance of the pipeline class
        self.inputBGRA = None  # input image variable
        self.outputBGRA = None  # output image variable
        self.curHistLayer = -1  # current histogram layer variable
        self.curColorLayer = -1  # current color layer variable
        self.histView = False  # histogram view variable
        self.yLim = 0  # y-axis limit variable for histogram
        self.zoomAmount = 0  # zoom amount variable for histogram


    def init_topLayout(self):
        """
        Initialize the top layout with two labels for displaying images.
        """
        # Create top layout and add it to the main layout
        topLayout = QHBoxLayout()
        self.mainLayout.addLayout(topLayout, 55)  

        # create leftLayout to hold the left image and title
        leftLayout = QVBoxLayout()
        leftLayout.setContentsMargins(0, 0, 0, 0)
        leftLayout.setSpacing(0)
        topLayout.addLayout(leftLayout, 6)

        # create leftTitle label for displaying the input image title
        self.leftTitle = QLabel("")
        leftLayout.addWidget(self.leftTitle, 0.5, alignment=Qt.AlignCenter)

        # Create leftLabel for displaying the input image
        self.leftLabel = QLabel(self)
        pixmap = QPixmap("images/no_image.jpg")
        self.leftLabel.setPixmap(pixmap)
        self.leftLabel.setAlignment(Qt.AlignCenter)
        leftLayout.addWidget(self.leftLabel, 12)

        # create spacer layout to separate the two labels
        spacer = QVBoxLayout()
        topLayout.addLayout(spacer, 1)

        # create zoom layout
        zoomLayout = QHBoxLayout()
        spacer.addLayout(zoomLayout, 1)
        font = QFont()              
        font.setPointSize(12)  

        # create zoom out button
        self.zoomOut = QPushButton("-")
        self.zoomOut.setFixedWidth(40)
        self.zoomOut.setFont(font) 
        self.zoomOut.setStyleSheet("padding-bottom: 2px;")
        self.zoomOut.clicked.connect(lambda: self.display_histogram(zoom=-1)) 
        zoomLayout.addWidget(self.zoomOut, 1, alignment=Qt.AlignBottom)
        self.zoomOut.hide()
        
        # create zoom in button
        self.zoomIn = QPushButton("+")
        self.zoomIn.setFixedWidth(40)
        self.zoomIn.setFont(font) 
        self.zoomIn.setStyleSheet("padding-bottom: 2px;")
        self.zoomIn.clicked.connect(lambda: self.display_histogram(zoom=1))
        zoomLayout.addWidget(self.zoomIn, 1, alignment=Qt.AlignBottom)
        self.zoomIn.hide()
        
        # create spacer label
        arrow = QLabel(">")
        font = QFont()              
        font.setPointSize(35)       
        arrow.setFont(font) 
        arrow.setAlignment(Qt.AlignCenter)  
        spacer.addWidget(arrow, 1, alignment=Qt.AlignTop)

        # create rightLayout to hold the right image and title
        rightLayout = QVBoxLayout()
        rightLayout.setContentsMargins(0, 0, 0, 0)
        rightLayout.setSpacing(0)
        topLayout.addLayout(rightLayout, 6)

        # create rightTitle label for displaying the output image title
        self.rightTitle = QLabel("")
        rightLayout.addWidget(self.rightTitle, 0.5, alignment=Qt.AlignCenter)

        # Create rightLabel for displaying the output image
        self.rightLabel = QLabel(self)
        pixmap = QPixmap("images/no_image.jpg")
        self.rightLabel.setPixmap(pixmap)
        self.rightLabel.setAlignment(Qt.AlignCenter)
        rightLayout.addWidget(self.rightLabel, 12)


    def init_midLayout(self):
        """
        Initialize the mid layout with buttons for various actions.
        """
        # Create mid layout and add it to the main layout
        midLayout = QHBoxLayout()
        self.mainLayout.addLayout(midLayout, 10) 

        # Create mid layout widgets and add them to the mid layout
        font = QFont()              
        font.setPointSize(10)  
        
        # Button 1 - open image
        btn = QPushButton(constants.OPEN_BUTTON)
        midLayout.addWidget(btn)      
        btn.clicked.connect(self.select_image)   
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 2 - switch to histogram
        btn = QPushButton(constants.HISTOGRAM_BUTTON)
        midLayout.addWidget(btn)    
        btn.clicked.connect(self.switch_to_histogram)   
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 3 - See Layers
        btn = QPushButton(constants.CHANNELS_BUTTON)
        midLayout.addWidget(btn)    
        btn.clicked.connect(self.switch_to_colorLayer)  
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 4 - switch to frequency domain
        btn = QPushButton(constants.FREQUENCY_BUTTON)
        midLayout.addWidget(btn)    
        btn.clicked.connect(self.switch_to_frequency)  
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 5 - save image
        btn = QPushButton(constants.SAVE_BUTTON)
        midLayout.addWidget(btn)   
        btn.clicked.connect(lambda: utils.save_image(self.outputBGRA))   
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 


    def init_bottomLayout(self):
        """
        Initialize the bottom layout with scroll area for function boxes.
        """
        # Create bottom layout and add it to the main layout
        bottomLayout = QHBoxLayout()
        self.mainLayout.addLayout(bottomLayout, 35)
          
        # create scroll area widget and add it to the bottom layout
        scrollArea = QScrollArea()         
        scrollArea.setWidgetResizable(True)        
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
        bottomLayout.addWidget(scrollArea)        
        
        # create content widget and set it to the scroll area
        contentWidget = QWidget()  
        scrollArea.setWidget(contentWidget)  

        # create content layout and set it to the content widget
        self.contentLayout = QHBoxLayout(contentWidget)
        self.contentLayout.setAlignment(Qt.AlignLeft)
                
        # insert 'new function' box
        self.addNewBox = toolboxes.AddNewBox()
        self.contentLayout.addWidget(self.addNewBox)
        self.addNewBox.trigger.connect(self.add_new_func)  # connect signal to the slot

        # drag and drop functionality
        contentWidget.setAcceptDrops(True)
        contentWidget.dragEnterEvent = self.dragEnterEvent
        contentWidget.dropEvent = self.dropEvent


    def dragEnterEvent(self, event):
        """
        Handle the drag enter event to allow drag-and-drop functionality.

        Args:
            event (QDragEnterEvent): The drag enter event containing information about the dragged data.
        """
        # Check if the event contains mime data and accept the proposed action
        if event.mimeData():
            event.acceptProposedAction()


    def dropEvent(self, event):
        """
        Handle the drop event to allow reordering of function boxes in the pipeline.

        Args:
            event (QDropEvent): The drop event containing information about the dropped data.
        """
        # Get the position where the item is dropped
        pos = event.position().toPoint()
        # Get the source widget being dragged
        source = event.source()
        # Find the index where the item should be inserted
        index = self.find_insert_index(pos)

        # Check if the source is a valid FunctionBox
        if source and isinstance(source, toolboxes.FunctionBox):
            self.pipeline.move_step(source, index)  # move the function box in the pipeline
            
            # Remove the widget from its current position in the layout
            self.contentLayout.removeWidget(source)
            # Insert the widget at the new index in the layout
            self.contentLayout.insertWidget(index, source)

            # Accept the proposed action for the drop event
            event.acceptProposedAction()

            # Rerun the pipeline to update the output image
            self.process_pipeline()


    def find_insert_index(self, pos):
        """
        Find the index in the layout where a widget should be inserted based on the drop position.

        Args:
            pos (QPoint): The position where the item is dropped.

        Returns:
            int: The index where the widget should be inserted.
        """
        # Iterate through all widgets in the content layout
        for i in range(self.contentLayout.count()):
            widget = self.contentLayout.itemAt(i).widget()
            # Check if the widget is valid and not the special footer widget (addNewBox)
            if widget and widget != self.addNewBox:
                # If the drop position is within the geometry of the widget, return its index
                if widget.geometry().contains(pos):
                    return i
        # If no suitable position is found, return the last index (before addNewBox)
        return self.contentLayout.count() - 1


    @Slot(str)
    def add_new_func(self, functionName):
        """
        This function is called when a new function box is added.
        It creates a new function box and adds it to the content layout.
        """
        # Create a new function box based on the selected function name
        if functionName == constants.BRIGHTNESS_NAME:
            newBox = toolboxes.BrightnessBox()
        elif functionName == constants.SATURATION_NAME:
            newBox = toolboxes.SaturationBox()
        elif functionName == constants.CONTRAST_NAME:
            newBox = toolboxes.ContrastBox()
        elif functionName == constants.FULL_SCALE_CONTRAST_NAME:
            newBox = toolboxes.FullScaleContrastBox()
        elif functionName == constants.LOG_NAME:
            newBox = toolboxes.LogBox()
        elif functionName == constants.GAMMA_NAME:
            newBox = toolboxes.GammaBox()
        elif functionName == constants.RGB2GRAY_NAME:
            newBox = toolboxes.RGB2GrayBox()
        elif functionName == constants.THRESHOLDING_NAME:
            newBox = toolboxes.ThresholdingBox()
        elif functionName == constants.COMPLEMENT_NAME:
            newBox = toolboxes.ComplementBox()
        elif functionName == constants.CROP_NAME:
            newBox = toolboxes.CropBox()    
        elif functionName == constants.FLIP_NAME:
            newBox = toolboxes.FlipBox()
        elif functionName == constants.ROTATE_NAME:
            newBox = toolboxes.RotateBox()
        elif functionName == constants.RESIZE_NAME:
            newBox = toolboxes.ResizeBox()
        elif functionName == constants.PADDING_NAME:
            newBox = toolboxes.PaddingBox()
        elif functionName == constants.HISTEQ_NAME:
            newBox = toolboxes.HistEqualizationBox()
        elif functionName == constants.HISTCLAHE_NAME:
            newBox = toolboxes.HistCLAHEBox()
        elif functionName == constants.MASK_NAME:
            newBox = toolboxes.MaskBox()
        elif functionName == constants.BITSLICE_NAME:
            newBox = toolboxes.BitSliceBox()
        elif functionName == constants.ADD_NOISE_NAME:
            newBox = toolboxes.NoiseBox()
        elif functionName == constants.ARITHMETIC_NAME:
            newBox = toolboxes.ArithmeticBox()
        elif functionName == constants.LOGIC_NAME:
            newBox = toolboxes.LogicBox()
        elif functionName == constants.LAPLACE_NAME:
            newBox = toolboxes.LaplaceBox()
        elif functionName == constants.SOBEL_NAME:
            newBox = toolboxes.SobelBox()
        elif functionName == constants.SPATIAL_NAME:
            newBox = toolboxes.SpatialFilterBox()
        
        self.pipeline.add_step(newBox)                              # add the new function box to the pipeline
        newBox.updateTrigger.connect(self.process_pipeline)      # connect the process signal to the ProcessPipeline function
        newBox.removeTrigger.connect(self.remove_func)           # connect the remove signal to the RemoveFunc function

        self.contentLayout.removeWidget(self.addNewBox)         # remove the special footer widget (addNewBox) from the layout
        self.addNewBox.setParent(None)
        self.contentLayout.addWidget(newBox)                    # add the new function box to the layout
        self.contentLayout.addWidget(self.addNewBox)            # add the special footer widget (addNewBox) back to the layout

        self.process_pipeline()                                  # rerun the pipeline to update the output image

    
    @Slot(str)
    def remove_func(self, functionName):
        """
        This function is called when a function box is removed.
        It removes the function box from the pipeline and the layout.
        """
        self.pipeline.remove_step(functionName)  # remove the function box from the pipeline
        
        # remove the function box from the layout
        for i in range(self.contentLayout.count()):
            widget = self.contentLayout.itemAt(i).widget()
            if widget and widget.title == functionName:
                self.contentLayout.removeWidget(widget)
                widget.setParent(None)
                break
        
        # rerun the pipeline to update the output image
        self.process_pipeline()
        

    @Slot()
    def process_pipeline(self):
        """
        This function is called to process the image through the function boxes.
        """        
        if self.inputBGRA is None:
            return                                      # if no image is loaded, return
        

        try:
            self.outputBGRA = self.pipeline.run(self.inputBGRA)                     # run the pipeline on the input image

            # update the output image
            if self.histView:
                self.display_histogram()
            elif self.curColorLayer != -1:
                self.display_color_layer()
            else:
                self.image_pixmap(self.outputBGRA, self.rightLabel)
        
        except Exception as e:
            QMessageBox.information(self, "Error", traceback.format_exc())


    @Slot() 
    def select_image(self):

        image = utils.select_image()     # read the image

        if image is not None:
            # reinitialize variables since a new image is opened
            self.init_variables()
            self.zoomIn.hide()  # deactivate zoom buttons
            self.zoomOut.hide()     

            self.inputBGRA = image.copy()          # make a copy of the input image
            self.outputBGRA = self.inputBGRA.copy()          # make a copy of the input image for output

            # display the image
            self.image_pixmap(self.inputBGRA, self.leftLabel)  
            self.image_pixmap(self.inputBGRA, self.rightLabel)  

            # process the image through the pipeline
            self.process_pipeline()  



    @Slot() 
    def switch_to_histogram(self):
        """
        Switch between displaying the image and its histogram in the labels.
        """
        try:
            
            # if the last layer is reached, switch back to image view 
            if self.curHistLayer+1 >= 4:
                self.curHistLayer = -1
                self.histView = False
                self.zoomIn.hide()      # deactivate zoom buttons
                self.zoomOut.hide()
                self.zoomAmount = 0
                self.image_pixmap(self.inputBGRA, self.leftLabel)  
                self.image_pixmap(self.outputBGRA, self.rightLabel)
            
            # else, display the histogram of the current layer
            else:
                self.curHistLayer += 1
                self.histView = True
                self.zoomIn.show()          # activate zoom buttons
                self.zoomOut.show()
                self.display_histogram()     

        except Exception as e:
            QMessageBox.information(self, "Error", f"{e}")


    def display_histogram(self, zoom=0):
        """
        Display the histogram of the input and output images in the left and right labels respectively.
        """
        # reset color layer index
        self.curColorLayer = -1  

        bgra2rgba = [2, 1, 0, 3]  # OpenCV reads images in BGR format
        ascImgIn = np.ascontiguousarray(self.inputBGRA[:,:,bgra2rgba[self.curHistLayer]])
        ascImgOut = np.ascontiguousarray(self.outputBGRA[:,:,bgra2rgba[self.curHistLayer]])
        self.histogram_pixmap(ascImgIn, self.leftLabel, zoom)
        self.histogram_pixmap(ascImgOut, self.rightLabel)        # no needed zoom parameter in the second call


    @Slot() 
    def switch_to_colorLayer(self):
        try:
            # if the last color layer is reached, switch back to original view 
            if self.curColorLayer+1 >= 4:
                    self.curColorLayer = -1
                    self.image_pixmap(self.inputBGRA, self.leftLabel)  
                    self.image_pixmap(self.outputBGRA, self.rightLabel)
                    # change the text of leftTitle and rightTitle to empty string
                    self.leftTitle.setText("")
                    self.rightTitle.setText("")
            
            # else, display the current color layer
            else:
                self.curColorLayer += 1
                self.display_color_layer()  

        except Exception as e:
            QMessageBox.information(self, "Error", f"{e}")


    def display_color_layer(self):
        """
        Display the current color layer of the input and output images in the left and right labels respectively.
        """
        # reset histogram view
        self.histView = False
        self.curHistLayer = -1
        self.zoomIn.hide()          # deactivate zoom buttons
        self.zoomOut.hide()

        bgra2rgba = [2, 1, 0, 3]  # OpenCV reads images in BGRA format
        ascImgIn = np.ascontiguousarray(self.inputBGRA[:,:,bgra2rgba[self.curColorLayer]])
        ascImgOut = np.ascontiguousarray(self.outputBGRA[:,:,bgra2rgba[self.curColorLayer]])
        self.image_pixmap(ascImgIn, self.leftLabel, title=True)
        self.image_pixmap(ascImgOut, self.rightLabel, title=True)


    @Slot() 
    def switch_to_frequency(self):
        """
        Switch between displaying the image and its frequency domain representation.
        """
        try:
            pass

        except Exception as e:
            QMessageBox.information(self, "Error", f"{e}")


    def image_pixmap(self, image, label, title=False):
        """
        Convert a NumPy image array to QPixmap and display it in the given QLabel.

        Args:
            image (numpy.ndarray): The input image as a NumPy array. It can be grayscale or color.
            label (QLabel): The QLabel widget where the image will be displayed.
            title (bool): Whether to set the title for the QLabel. Default is False.
        """
        # set the title if enabled
        if title:
            self.leftTitle.setText(f"{CHANNEL_NAMES[self.curColorLayer]} Channel")
            self.rightTitle.setText(f"{CHANNEL_NAMES[self.curColorLayer]} Channel")
        else:
            self.leftTitle.setText("")
            self.rightTitle.setText("")

        # Convert NumPy array to QImage
        height, width = image.shape[:2]

        # Convert BGRA to RGBA
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
        qimg = QImage(image.data, width, height, image.strides[0], QImage.Format_RGBA8888)

        # Set the QImage to the QLabel
        pixmap = QPixmap.fromImage(qimg) 
        scaled = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(scaled)


    def histogram_pixmap(self, image, label, zoom=0):
        """
        Display the histogram of the given image in the specified QLabel.

        Args:
            image (numpy.ndarray): The input image as a NumPy array.
            label (QLabel): The QLabel widget where the histogram will be displayed.
        """
        self.zoomAmount += zoom         # update the zoom amount 
        fig, ax = plt.subplots()        # Create a new figure for the histogram
        histNums = ax.hist(image.ravel(), bins=100, color='black')      # Plot the histogram

        # set y-axis limit and step
        if self.yLim == 0 or self.yLim < np.max(histNums[0]) or self.lastLayer != self.curHistLayer:
            self.yLim = np.max(histNums[0]) * 1.2       # set y-axis limit to 20% more than max value
            self.yStep = self.yLim / 5 
            self.lastLayer = self.curHistLayer
        
        # Set style and labels
        ax.grid(True)
        ax.set_xlim(0, 255)
        ax.set_ylim(0, self.yLim)
        ax.set_xticks(np.append(np.arange(0, 250, 25), 255))
        ax.set_yticks(np.arange(0, self.yLim+1, self.yStep))
        
        # Set y-axis limits based on zoom amount
        if self.zoomAmount != 0:
            zoom_factor = 1 / (1 + self.zoomAmount * 0.3)  
            yLim = round(self.yLim * zoom_factor)
            ax.set_ylim(0, yLim)
            ax.set_yticks(np.int16(np.arange(0, yLim+1, yLim / 5)))

        # set title based on the color format and layer
        ax.set_title(f"{CHANNEL_NAMES[self.curHistLayer]} Channel")

        # Save the figure to a BytesIO buffer
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        plt.close(fig)

        # Convert the buffer to QImage and set it to the QLabel
        buf.seek(0)
        qimg = QImage.fromData(buf.getvalue())
        pixmap = QPixmap.fromImage(qimg)
        pixmap = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)

