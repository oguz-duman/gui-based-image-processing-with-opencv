import cv2
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import traceback

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QMessageBox, QFileDialog

import constants
from ui import toolboxes
from constants import CHANNEL_NAMES
from processing.pipeline import Pipeline


class UiManagement():
    """
    This class manages the UI elements and interactions for the image processing application.
    It handles image loading, toolbox insertion and deletion, histogram display, color layer switching, image saving and displaying.
    """
    def __init__(self):
        self.init_variables()

    def init_ui_variables(self, toolbox_wrapper, footer_toolbox, leftLabel, 
                          rightLabel, leftTitle, rightTitle, zoomIn, zoomOut):
        """
        Initialize the UI variables used in the application.
        Args:
            toolbox_wrapper (QVBoxLayout): The layout where the toolboxes are added.
            footer_toolbox (QWidget): The footer widget for the toolbox layout.
            leftLabel (QLabel): The label for displaying the input image.
            rightLabel (QLabel): The label for displaying the output image.
            leftTitle (QLabel): The label for displaying the title of the input image.
            rightTitle (QLabel): The label for displaying the title of the output image.
            zoomIn (QPushButton): The button for zooming in on the histogram.
            zoomOut (QPushButton): The button for zooming out on the histogram.
        """
        self.toolbox_wrapper = toolbox_wrapper
        self.footer_toolbox = footer_toolbox
        self.leftLabel = leftLabel
        self.rightLabel = rightLabel
        self.leftTitle = leftTitle
        self.rightTitle = rightTitle
        self.zoomIn = zoomIn
        self.zoomOut = zoomOut

        # Initialize the pipeline
        self.pipeline = Pipeline()  

        # Modes and their corresponding methods which are called when the mode is activated
        self.mode_handlers = {      
            'IMAGE': lambda: self.display_image([self.input_BGRA, self.output_BGRA]),  
            'HISTOGRAM': lambda: self.display_histogram(self.zoomAmount),
            'CHANNELS': lambda: self.display_image(self.get_color_channels()),  
            'FREQUENCY': None
        }
        # Decide which widgets to show or hide when the mode is changed
        self.widgets_per_mode = {
            'IMAGE': [],
            'HISTOGRAM': [self.zoomIn, self.zoomOut],
            'CHANNELS': [self.leftTitle, self.rightTitle],
            'FREQUENCY': []
        }


    def init_variables(self):
        """
        Initialize the variables used in the ui.
        """
        self.input_BGRA = None                      # input image variable
        self.output_BGRA = None                     # output image variable
        
        self.active_mode = 'IMAGE'                  # current mode mode variable
        self.channel_index = 0                      # current color layer variable
        
        self.y_lim = 0                              # y-axis limit variable for histogram
        self.zoomAmount = 0                         # zoom amount variable for histogram
        
        
    def open_new_image(self):
        """
        Open a new image using a file dialog and update the input and output images.
        This method is called when the "Open Image" button is clicked.
        It allows the user to select an image file and processes it through the pipeline.
        """
        image = self.select_image()            # select an image using the file dialog

        if image is not None:
            self.init_variables()               # reinitialize variables since a new image is opened

            self.input_BGRA = image.copy()       # make a copy of the input image for input
            self.output_BGRA = image.copy()      # make a copy of the input image for output

            # display the input and output images in the labels
            self.display_image([self.input_BGRA, self.output_BGRA])  

            self.pipeline_on_change()           # process the image through the pipeline


    def select_image(self):
        """
        Open a file dialog to select an image file and read it using OpenCV.
        Returns:
            image (np.ndarray): The selected image as a NumPy array.
        """
        # Open file dialog to select an image file
        filePath, _ = QFileDialog.getOpenFileName(None, "Select an image file", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp)")

        # Check if a file was selected
        if filePath:
            image = cv2.imread(filePath, cv2.IMREAD_UNCHANGED)      # read the image
            
            if image is None:
                raise ValueError("No input image provided")
            elif len(image.shape) == 2:                             # if image is (h,w)
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)
            elif len(image.shape) == 3 and image.shape[2] == 1:     # if image is (h,w,1)
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)
            elif len(image.shape) == 3 and image.shape[2] == 3:     # if image is (BGR) (h,w,3)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
            elif len(image.shape) == 3 and image.shape[2] == 4:     # if image is (BGRA) (h,w,4)
                pass
            else:
                raise ValueError("Unsupported image format")
            
            return image
    
    
    @Slot(str)
    def insert_toolbox(self, toolbox):
        """
        Add a new method box to the pipeline and the layout based on the selected method name.
        Args:
            toolbox (str): The name of the method to be added.
        """
        # Create a new method box based on the selected method name
        if toolbox == constants.BRIGHTNESS_NAME:
            new_toolbox = toolboxes.BrightnessBox()
        elif toolbox == constants.SATURATION_NAME:
            new_toolbox = toolboxes.SaturationBox()
        elif toolbox == constants.CONTRAST_NAME:
            new_toolbox = toolboxes.ContrastBox()
        elif toolbox == constants.FULL_SCALE_CONTRAST_NAME:
            new_toolbox = toolboxes.FullScaleContrastBox()
        elif toolbox == constants.LOG_NAME:
            new_toolbox = toolboxes.LogBox()
        elif toolbox == constants.GAMMA_NAME:
            new_toolbox = toolboxes.GammaBox()
        elif toolbox == constants.RGB2GRAY_NAME:
            new_toolbox = toolboxes.RGB2GrayBox()
        elif toolbox == constants.THRESHOLDING_NAME:
            new_toolbox = toolboxes.ThresholdingBox()
        elif toolbox == constants.COMPLEMENT_NAME:
            new_toolbox = toolboxes.ComplementBox()
        elif toolbox == constants.CROP_NAME:
            new_toolbox = toolboxes.CropBox()    
        elif toolbox == constants.FLIP_NAME:
            new_toolbox = toolboxes.FlipBox()
        elif toolbox == constants.ROTATE_NAME:
            new_toolbox = toolboxes.RotateBox()
        elif toolbox == constants.RESIZE_NAME:
            new_toolbox = toolboxes.ResizeBox()
        elif toolbox == constants.PADDING_NAME:
            new_toolbox = toolboxes.PaddingBox()
        elif toolbox == constants.HISTEQ_NAME:
            new_toolbox = toolboxes.HistEqualizationBox()
        elif toolbox == constants.HISTCLAHE_NAME:
            new_toolbox = toolboxes.HistCLAHEBox()
        elif toolbox == constants.MASK_NAME:
            new_toolbox = toolboxes.MaskBox()
        elif toolbox == constants.BITSLICE_NAME:
            new_toolbox = toolboxes.BitSliceBox()
        elif toolbox == constants.ADD_NOISE_NAME:
            new_toolbox = toolboxes.NoiseBox()
        elif toolbox == constants.ARITHMETIC_NAME:
            new_toolbox = toolboxes.ArithmeticBox()
        elif toolbox == constants.LOGIC_NAME:
            new_toolbox = toolboxes.LogicBox()
        elif toolbox == constants.LAPLACE_NAME:
            new_toolbox = toolboxes.LaplaceBox()
        elif toolbox == constants.SOBEL_NAME:
            new_toolbox = toolboxes.SobelBox()
        elif toolbox == constants.SPATIAL_NAME:
            new_toolbox = toolboxes.SpatialFilterBox()
        else:
            raise ValueError("Invalid method name. You may have forgotten to add the relevant " \
            "toolbox to the 'add_new_func' method in the main_window.py.")
        
        # connect the toolbox signals
        new_toolbox.updateTrigger.connect(self.pipeline_on_change)   
        new_toolbox.removeTrigger.connect(self.remove_toolbox) 

        self.pipeline.add_step(new_toolbox)                             # add the toolbox to the pipeline

        self.toolbox_wrapper.removeWidget(self.footer_toolbox)      # remove the special footer widget
        self.footer_toolbox.setParent(None)           
        self.toolbox_wrapper.addWidget(new_toolbox)                     # add the toolbox to the layout
        self.toolbox_wrapper.addWidget(self.footer_toolbox)         # add the special footer widget back

        self.pipeline_on_change()                                   # trigger the update method to rerun the updated pipeline 


    @Slot(str)
    def remove_toolbox(self, toolbox):
        """
        Remove the method box from the pipeline and the layout.
        Args:
            toolbox (str): The name of the method to be removed.
        """
        # remove the method box from the layout
        for i in range(self.toolbox_wrapper.count()):
            widget = self.toolbox_wrapper.itemAt(i).widget()
            if widget and widget.title == toolbox:
                self.toolbox_wrapper.removeWidget(widget)
                widget.setParent(None)
                break
        
        self.pipeline.remove_step(toolbox)         # remove the method box from the pipeline
        self.pipeline_on_change()                  # rerun the pipeline to update the output image
   

    def pipeline_on_change(self):
        """
        """
        if self.input_BGRA is not None:
            self.output_BGRA = self.pipeline.run(self.input_BGRA)              # run the pipeline on the input image

            # update the ui based on the current mode
            if self.active_mode == 'IMAGE':
                self.display_image([self.input_BGRA, self.output_BGRA])
            elif self.active_mode == 'HISTOGRAM':
                self.display_histogram()
            elif self.active_mode == 'CHANNELS':
                self.display_image(self.get_color_channels())
            elif self.active_mode == 'FREQUENCY':
                self.display_image(self.get_color_channels())
       

    def mode_buttons(self, mode_name):
        """
        """
        if self.input_BGRA is None:
            return
        elif not self.active_mode == mode_name:
            self.switch_mode(mode_name)   
            self.mode_handlers[mode_name]()          # call the method corresponding to the mode name             
        else:
            self.channel_index = self.channel_index + 1 if self.channel_index < len(CHANNEL_NAMES) else 0       # increment the channel index 
            if self.channel_index == 0:
                self.switch_mode('IMAGE')  
                self.display_image([self.input_BGRA, self.output_BGRA])
            else:
                self.mode_handlers[mode_name]()          # call the method corresponding to the mode name             


    def switch_mode(self, mode_name):
        """
        """
        self.active_mode = mode_name                # active mode name
        self.channel_index = 0                      # reset channel index
        self.zoomAmount = 0                         # reset zoom amount

        # show or hide the relevant widgets based on the selected mode
        for w in self.widgets_per_mode.keys():
            if w == mode_name:
                for widget in self.widgets_per_mode[w]:
                    widget.show()
            else:
                for widget in self.widgets_per_mode[w]:
                    widget.hide()
           

    def display_image(self, images):
        """
        """
        # set the title to current color channel
        self.leftTitle.setText(f"{CHANNEL_NAMES[self.channel_index]} Channel")
        self.rightTitle.setText(f"{CHANNEL_NAMES[self.channel_index]} Channel")

        for image, label in zip(images, [self.leftLabel, self.rightLabel]):
            # Convert BGRA to RGBA
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
            qimg = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGBA8888)

            # Set the QImage to the QLabel
            pixmap = QPixmap.fromImage(qimg) 
            scaled = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(scaled)

 
    def display_histogram(self, zoom=0):
        """
        """
        self.zoomAmount += zoom                                         # update the zoom amount if a zoom amount is passed

        for image, label in zip(self.get_color_channels(), [self.leftLabel, self.rightLabel]):
            fig, ax = plt.subplots()                                        # Create a new figure for the histogram
            histNums = ax.hist(image.ravel(), bins=100, color='black')      # Plot the histogram
            # set y-axis limit and step
            if self.y_lim == 0 or self.y_lim < np.max(histNums[0]):
                self.y_lim = np.max(histNums[0]) * 1.2       # set y-axis limit to 20% more than max value
                self.yStep = self.y_lim / 5 
                
            # Set style and labels
            ax.grid(True)
            ax.set_xlim(0, 255)
            ax.set_ylim(0, self.y_lim)
            ax.set_xticks(np.append(np.arange(0, 250, 25), 255))
            ax.set_yticks(np.arange(0, self.y_lim+1, self.yStep))
            
            # Overwrite the y-axis limit and ticks if the zoom amount is not 0 
            if self.zoomAmount != 0:
                zoom_factor = 1 / (1 + self.zoomAmount * 0.3)  
                yLim = round(self.y_lim * zoom_factor)
                ax.set_ylim(0, yLim)
                ax.set_yticks(np.int16(np.arange(0, yLim+1, yLim / 5)))

            # set title based on the RGBA color format and current channel
            ax.set_title(f"{CHANNEL_NAMES[self.channel_index]} Channel")

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


    def get_color_channels(self):
        """
        """
        bgra2rgba = [2, 1, 0, 3]                        # OpenCV reads images in BGRA format
        return [
            self.input_BGRA[:,:,bgra2rgba[self.channel_index]], 
            self.output_BGRA[:,:,bgra2rgba[self.channel_index]]
        ]                    


    def save_image(self):
        """
        Open a file dialog to select a file path to save the image.
        Args:
            image (np.ndarray): The image to be saved.
        """
        # Open file dialog to select a file path to save the image
        filePath, _ = QFileDialog.getSaveFileName(None, "Save the image", "", "Image Files (*.jpg *.jpeg *.png *.bmp *.gif *.tif *.tiff *.webp)")
        
        # Check if a file path was selected
        if filePath:
            try:
                cv2.imwrite(filePath, self.output_BGRA)            # Save the image using OpenCV
            except Exception as e:
                QMessageBox.information(None, "Error", f"Failed to save the image.\n{str(e)}")


