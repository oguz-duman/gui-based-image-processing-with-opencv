import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import traceback

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap, QFont, QImage
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QScrollArea,
    QFileDialog, QMessageBox
)

# Import custom function boxes
import functions


# -------------------------- main class definitions -------------------

class MainWidget(QWidget):

    def __init__(self):
        super().__init__()  

        self.pipeline = []  # pipeline variable to store function boxes
        self.InitVariables()  # Initialize variables
        self.InitUi()      # Initialize UI
        

    def InitUi(self):
        """
        Initialize the UI components and layout.
        """
        # Create main layout and set it to the widget
        self.mainLayout = QVBoxLayout(self) 
        self.mainLayout.setContentsMargins(20, 5, 20, 5) 
        self.mainLayout.setSpacing(15)

        # init top, mid and bottom layouts
        self.InitTopLayout()
        self.InitMidLayout()
        self.InitBottomLayout()


    def InitVariables(self):
        """
        Initialize the variables used in the widget.
        """
        self.inputImg = None  # input image variable
        self.outputImg = None  # output image variable
        self.curHistLayer = -1  # current histogram layer variable
        self.curColorLayer = -1  # current color layer variable
        self.histView = False  # histogram view variable
        self.yLim = 0  # y-axis limit variable for histogram
        self.zoomAmount = 0  # zoom amount variable for histogram
        self.channelNames = ["Red", "Green", "Blue", "Alpha"]    # channel names variable


    def InitTopLayout(self):
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
        self.zoomOut.clicked.connect(lambda: self.DisplayHistogram(zoom=-1)) 
        zoomLayout.addWidget(self.zoomOut, 1, alignment=Qt.AlignBottom)
        self.zoomOut.hide()
        
        # create zoom in button
        self.zoomIn = QPushButton("+")
        self.zoomIn.setFixedWidth(40)
        self.zoomIn.setFont(font) 
        self.zoomIn.setStyleSheet("padding-bottom: 2px;")
        self.zoomIn.clicked.connect(lambda: self.DisplayHistogram(zoom=1))
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


    def InitMidLayout(self):
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
        btn = QPushButton(f"Open")
        midLayout.addWidget(btn)      
        btn.clicked.connect(self.OpenImage)   
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 2 - switch to histogram
        btn = QPushButton(f"Histogram")
        midLayout.addWidget(btn)    
        btn.clicked.connect(self.SwitchToHistogram)   
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 3 - See Layers
        btn = QPushButton(f"Channels")
        midLayout.addWidget(btn)    
        btn.clicked.connect(self.SwitchToColorLayer)  
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 4 - switch to frequency domain
        btn = QPushButton(f"Frequency")
        midLayout.addWidget(btn)    
        btn.clicked.connect(self.SwitchToFrequency)  
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 5 - save image
        btn = QPushButton(f"Save")
        midLayout.addWidget(btn)   
        btn.clicked.connect(self.SaveImage)   
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 


    def InitBottomLayout(self):
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
        self.addNewBox = functions.AddNewBox()
        self.contentLayout.addWidget(self.addNewBox)
        self.addNewBox.trigger.connect(self.AddNewFunc)  # connect signal to the slot

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
        index = self.findInsertIndex(pos)

        # Check if the source is a valid FunctionBox
        if source and isinstance(source, functions.FunctionBox):
            # Move the function box to the new index in the pipeline
            self.moveFunctionBox(source, index)
            # Accept the proposed action for the drop event
            event.acceptProposedAction()

            # Rerun the pipeline to update the output image
            self.ProcessPipeline()


    def findInsertIndex(self, pos):
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


    def moveFunctionBox(self, widget, index):
        """
        Move a function box widget to a new position in the pipeline and layout.

        Args:
            widget (QWidget): The function box widget to move.
            index (int): The new index position in the pipeline and layout.
        """
        # Check if the widget is in the pipeline
        if widget in self.pipeline:
            # Remove the widget from its current position in the pipeline
            self.pipeline.remove(widget)
            # Insert the widget at the new index in the pipeline
            self.pipeline.insert(index, widget)
            # Remove the widget from its current position in the layout
            self.contentLayout.removeWidget(widget)
            # Insert the widget at the new index in the layout
            self.contentLayout.insertWidget(index, widget)


    @Slot(str)
    def AddNewFunc(self, functionName):
        """
        This function is called when a new function box is added.
        It creates a new function box and adds it to the content layout.
        """
        # Create a new function box based on the selected function name
        if functionName == functions.BRIGHTNESS_NAME:
            newBox = functions.BrightnessBox()
        elif functionName == functions.CONTRAST_NAME:
            newBox = functions.ContrastBox()
        elif functionName == functions.FULL_SCALE_CONTRAST_NAME:
            newBox = functions.FullScaleContrastBox()
        elif functionName == functions.LOG_NAME:
            newBox = functions.LogBox()
        elif functionName == functions.GAMMA_NAME:
            newBox = functions.GammaBox()
        elif functionName == functions.BLACK_AND_WHITE_NAME:
            newBox = functions.BlackAndWhiteBox()
        elif functionName == functions.COMPLEMENT_NAME:
            newBox = functions.ComplementBox()
        elif functionName == functions.CROP_NAME:
            newBox = functions.CropBox()    
        elif functionName == functions.FLIP_NAME:
            newBox = functions.FlipBox()
        elif functionName == functions.ROTATE_NAME:
            newBox = functions.RotateBox()
        elif functionName == functions.RESIZE_NAME:
            newBox = functions.ResizeBox()
        elif functionName == functions.PADDING_NAME:
            newBox = functions.PaddingBox()
        elif functionName == functions.HISTEQ_NAME:
            newBox = functions.HistEqualizationBox()
        elif functionName == functions.HISTCLAHE_NAME:
            newBox = functions.HistCLAHEBox()
        elif functionName == functions.BITSLICE_NAME:
            newBox = functions.BitSliceBox()
        elif functionName == functions.ADD_NOISE_NAME:
            newBox = functions.NoiseBox()
        elif functionName == functions.RGB2GRAY_NAME:
            newBox = functions.RGB2GrayBox()
        elif functionName == functions.ARITHMETIC_NAME:
            newBox = functions.ArithmeticBox()
        elif functionName == functions.LAPLACE_NAME:
            newBox = functions.LaplaceBox()
        elif functionName == functions.SOBEL_NAME:
            newBox = functions.SobelBox()
        elif functionName == functions.SPATIAL_NAME:
            newBox = functions.SpatialFilterBox()
        
        self.pipeline.append(newBox)                            # add the new function box to the pipeline
        newBox.updateTrigger.connect(self.ProcessPipeline)      # connect the process signal to the ProcessPipeline function
        newBox.removeTrigger.connect(self.RemoveFunc)           # connect the remove signal to the RemoveFunc function

        self.contentLayout.removeWidget(self.addNewBox)         # remove the special footer widget (addNewBox) from the layout
        self.addNewBox.setParent(None)
        self.contentLayout.addWidget(newBox)                    # add the new function box to the layout
        self.contentLayout.addWidget(self.addNewBox)            # add the special footer widget (addNewBox) back to the layout

        self.ProcessPipeline()                                  # rerun the pipeline to update the output image

    
    @Slot(str)
    def RemoveFunc(self, functionName):
        """
        This function is called when a function box is removed.
        It removes the function box from the pipeline and the layout.
        """
        # remove the function box from the pipeline
        for pipe in self.pipeline:
            if pipe.title == functionName:
                self.pipeline.remove(pipe)
                break
        
        # remove the function box from the layout
        for i in range(self.contentLayout.count()):
            widget = self.contentLayout.itemAt(i).widget()
            if widget and widget.title == functionName:
                self.contentLayout.removeWidget(widget)
                widget.setParent(None)
                break
        
        # rerun the pipeline to update the output image
        self.ProcessPipeline()
        

    @Slot()
    def ProcessPipeline(self):
        """
        This function is called to process the image through the function boxes.
        """        
        if self.inputImg is None:
            return                                      # if no image is loaded, return
        
        try:
            # convert image to HSVA format
            img = cv2.cvtColor(self.inputImg[:, :, :3], cv2.COLOR_BGR2HSV)  # convert the image to HSV format
            img_HSVA = cv2.merge((img, self.inputImg[:,:,3]))  # merge the alpha channel with the HSV image
            
            for pipe in self.pipeline:
                # check if the function box is activated
                if pipe.switch.isChecked():
                    img_HSVA = pipe.process(img_HSVA)             # call the process function of the function box
            
            self.outputImg = cv2.cvtColor(img_HSVA[:, :, :3], cv2.COLOR_HSV2BGR)    # convert image to BGR format
            self.outputImg = cv2.merge((self.outputImg, img_HSVA[:, :, 3]))  # merge the alpha channel with the BGR image

            # update the output image
            if self.histView:
                self.DisplayHistogram()
            elif self.curColorLayer != -1:
                self.DisplayColorLayer()
            else:
                self.ImagePixmap(self.outputImg, self.rightLabel)
        
        except Exception as e:
            QMessageBox.information(self, "Error", traceback.format_exc())


    @Slot() 
    def OpenImage(self):
        """
        Open a file dialog to select an image file and display it in the left label.
        """
        # Open file dialog to select an image file
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "Select an image file",
            "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp)"
        )

        # Check if a file was selected
        if filePath:
            # reinitialize variables since a new image is opened
            self.InitVariables()
            self.zoomIn.hide()  # deactivate zoom buttons
            self.zoomOut.hide()

            self.inputImg = cv2.imread(filePath, cv2.IMREAD_UNCHANGED)      # read the image
            self.inputImg = self.any2RGBA(self.inputImg)                    # convert the image to RGBA format
            
            self.outputImg = self.inputImg          # make a copy of the input image for output

            # display the image
            self.ImagePixmap(self.inputImg, self.leftLabel)  
            self.ImagePixmap(self.inputImg, self.rightLabel)  

            # process the image through the pipeline
            self.ProcessPipeline()  



    def any2RGBA(self, image):
        """
        Convert the input image to RGBA format if it is not already in that format.
        The function checks the number of channels in the input image and converts it accordingly.
        The function raises a ValueError if the input image is None or if the image format is unsupported.
        The function also handles grayscale images by converting them to RGBA format.
        """
        if image is None:
            raise ValueError("No input image provided")
            
        elif len(image.shape) == 2:  # if image is  (h,w)
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)

        elif len(image.shape) == 3 and image.shape[2] == 1:  # if image is (h,w,1)
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)

        elif len(image.shape) == 3 and image.shape[2] == 3:  # ig image is (BGR) (h,w,3)
            return cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        
        elif len(image.shape) == 3 and image.shape[2] == 4:  # if image is (BGRA) (h,w,4)
            return image

        else:
            raise ValueError("Unsupported image format")


    @Slot() 
    def SwitchToHistogram(self):
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
                self.ImagePixmap(self.inputImg, self.leftLabel)  
                self.ImagePixmap(self.outputImg, self.rightLabel)
            
            # else, display the histogram of the current layer
            else:
                self.curHistLayer += 1
                self.histView = True
                self.zoomIn.show()          # activate zoom buttons
                self.zoomOut.show()
                self.DisplayHistogram()     

        except Exception as e:
            QMessageBox.information(self, "Error", f"{e}")


    def DisplayHistogram(self, zoom=0):
        """
        Display the histogram of the input and output images in the left and right labels respectively.
        """
        # reset color layer index
        self.curColorLayer = -1  

        bgra2rgba = [2, 1, 0, 3]  # OpenCV reads images in BGR format
        ascImgIn = np.ascontiguousarray(self.inputImg[:,:,bgra2rgba[self.curHistLayer]])
        ascImgOut = np.ascontiguousarray(self.outputImg[:,:,bgra2rgba[self.curHistLayer]])
        self.HistogramPixmap(ascImgIn, self.leftLabel, zoom)
        self.HistogramPixmap(ascImgOut, self.rightLabel)        # no needed zoom parameter in the second call


    @Slot() 
    def SwitchToColorLayer(self):
        try:
            # if the last color layer is reached, switch back to original view 
            if self.curColorLayer+1 >= 4:
                    self.curColorLayer = -1
                    self.ImagePixmap(self.inputImg, self.leftLabel)  
                    self.ImagePixmap(self.outputImg, self.rightLabel)
                    # change the text of leftTitle and rightTitle to empty string
                    self.leftTitle.setText("")
                    self.rightTitle.setText("")
            
            # else, display the current color layer
            else:
                self.curColorLayer += 1
                self.DisplayColorLayer()  

        except Exception as e:
            QMessageBox.information(self, "Error", f"{e}")


    def DisplayColorLayer(self):
        """
        Display the current color layer of the input and output images in the left and right labels respectively.
        """
        # reset histogram view
        self.histView = False
        self.curHistLayer = -1
        self.zoomIn.hide()          # deactivate zoom buttons
        self.zoomOut.hide()

        bgra2rgba = [2, 1, 0, 3]  # OpenCV reads images in BGRA format
        ascImgIn = np.ascontiguousarray(self.inputImg[:,:,bgra2rgba[self.curColorLayer]])
        ascImgOut = np.ascontiguousarray(self.outputImg[:,:,bgra2rgba[self.curColorLayer]])
        self.ImagePixmap(ascImgIn, self.leftLabel, title=True)
        self.ImagePixmap(ascImgOut, self.rightLabel, title=True)


    @Slot() 
    def SwitchToFrequency(self):
        """
        Switch between displaying the image and its frequency domain representation.
        """
        try:
            pass

        except Exception as e:
            QMessageBox.information(self, "Error", f"{e}")


    @Slot() 
    def SaveImage(self):
        """
        Open a file dialog to save the output image.
        """
        # Open file dialog to select a file path to save the image
        filePath, _ = QFileDialog.getSaveFileName(
            self,
            "Save the image",
            "",
            "Image Files (*.jpg *.jpeg *.png *.bmp *.gif *.tif *.tiff *.webp)"
        )
        
        # Check if a file path was selected
        if filePath:
            try:
                # Save the image using OpenCV
                cv2.imwrite(filePath, self.outputImg)
            except:
                QMessageBox.information(self, "Error", f"Failed to save the image. Please try again.")


    def ImagePixmap(self, image, label, title=False):
        """
        Convert a NumPy image array to QPixmap and display it in the given QLabel.

        Args:
            image (numpy.ndarray): The input image as a NumPy array. It can be grayscale or color.
            label (QLabel): The QLabel widget where the image will be displayed.
            title (bool): Whether to set the title for the QLabel. Default is False.
        """
        # set the title if enabled
        if title:
            self.leftTitle.setText(f"{self.channelNames[self.curColorLayer]} Channel")
            self.rightTitle.setText(f"{self.channelNames[self.curColorLayer]} Channel")
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


    def HistogramPixmap(self, image, label, zoom=0):
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
        ax.set_title(f"{self.channelNames[self.curHistLayer]} Channel")

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



if __name__ == "__main__":
    app = QApplication([])    

    widget = MainWidget()     
    widget.resize(800, 600) 
    widget.show()       

    sys.exit(app.exec())        
