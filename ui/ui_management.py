import cv2
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import traceback
import os

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QMessageBox, QFileDialog

import constants
from ui import toolboxes
from constants import CHANNEL_NAMES
from processing.pipeline import Pipeline



class UiManagement():
    """
    """

    def init_ui_variables(self, toolbox_wrapper, footer_toolbox, leftLabel, 
                          rightLabel, leftTitle, rightTitle, zoomIn, zoomOut):
        """
        """
        self.toolbox_wrapper = toolbox_wrapper
        self.footer_toolbox = footer_toolbox
        self.pipeline = Pipeline()  

        self.leftLabel = leftLabel
        self.rightLabel = rightLabel
        self.leftTitle = leftTitle
        self.rightTitle = rightTitle
        self.zoomIn = zoomIn
        self.zoomOut = zoomOut


    def init_variables(self):
        """
        Initialize the variables used in the ui.
        """
        self.inputBGRA = None       # input image variable
        self.outputBGRA = None      # output image variable
        self.curHistLayer = -1      # current histogram layer variable
        self.curColorLayer = -1     # current color layer variable
        self.histView = False       # histogram view variable
        self.yLim = 0               # y-axis limit variable for histogram
        self.zoomAmount = 0         # zoom amount variable for histogram
        
        
    def open_new_image(self):
        """
        Open a new image using a file dialog and update the input and output images.
        This function is called when the "Open Image" button is clicked.
        It allows the user to select an image file and processes it through the pipeline.
        """
        image = self.select_image()            # select an image using the file dialog

        if image is not None:
            self.init_variables()               # reinitialize variables since a new image is opened
            self.zoomIn.hide()                  # deactivate zoom buttons
            self.zoomOut.hide()     

            self.inputBGRA = image.copy()       # make a copy of the input image for input
            self.outputBGRA = image.copy()      # make a copy of the input image for output

            # display the input and output images in the labels
            self.image_pixmap(self.inputBGRA, self.leftLabel)  
            self.image_pixmap(self.outputBGRA, self.rightLabel)  

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
        Add a new function box to the pipeline and the layout based on the selected function name.
        Args:
            functionName (str): The name of the function to be added.
        """
        # Create a new function box based on the selected function name
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
            raise ValueError("Invalid function name. You may have forgotten to add the relevant " \
            "toolbox to the 'add_new_func' function in the main_window.py.")
        
        # connect the toolbox signals
        new_toolbox.updateTrigger.connect(self.pipeline_on_change)   
        new_toolbox.removeTrigger.connect(self.remove_toolbox) 

        self.pipeline.add_step(new_toolbox)                             # add the toolbox to the pipeline

        self.toolbox_wrapper.removeWidget(self.footer_toolbox)      # remove the special footer widget
        self.footer_toolbox.setParent(None)           
        self.toolbox_wrapper.addWidget(new_toolbox)                     # add the toolbox to the layout
        self.toolbox_wrapper.addWidget(self.footer_toolbox)         # add the special footer widget back

        self.pipeline_on_change()                                   # trigger the update function to rerun the updated pipeline 


    @Slot(str)
    def remove_toolbox(self, toolbox):
        """
        Remove the function box from the pipeline and the layout.
        Args:
            functionName (str): The name of the function to be removed.
        """
        # remove the function box from the layout
        for i in range(self.toolbox_wrapper.count()):
            widget = self.toolbox_wrapper.itemAt(i).widget()
            if widget and widget.title == toolbox:
                self.toolbox_wrapper.removeWidget(widget)
                widget.setParent(None)
                break
        
        self.pipeline.remove_step(toolbox)         # remove the function box from the pipeline
        self.pipeline_on_change()                  # rerun the pipeline to update the output image
   

    def pipeline_on_change(self):
        """
        Run the pipeline on the input image and update the output image.     
        This function is called whenever a function box is added, removed, or modified.
        It processes the input image through the pipeline and updates the output image.       
        """
        if self.inputBGRA is not None:
            try:
                # run the pipeline on the input image
                self.outputBGRA = self.pipeline.run(self.inputBGRA)                     

                # update the output image
                if self.histView:
                    self.display_histogram()
                elif self.curColorLayer != -1:
                    self.display_color_layer()
                else:
                    self.image_pixmap(self.outputBGRA, self.rightLabel)
            
            except:
                QMessageBox.information(self, "Error", traceback.format_exc())

 

    def image_pixmap(self, image, label, title=False):
        """
        Convert a NumPy image array to QPixmap and display it in the given QLabel.
        Args:
            image (numpy.ndarray): The input image as a NumPy array. It can be grayscale or color.
            label (QLabel): The QLabel widget where the image will be displayed.
            title (bool): Whether to set the title for the QLabel. Default is False. If True, the title will be set to the current color layer.
        """
        # set the title to current color layer name if the 'title' argument is True
        if title:
            self.leftTitle.setText(f"{CHANNEL_NAMES[self.curColorLayer]} Channel")
            self.rightTitle.setText(f"{CHANNEL_NAMES[self.curColorLayer]} Channel")
        else:
            self.leftTitle.setText("")
            self.rightTitle.setText("")

        # Convert BGRA to RGBA
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
        qimg = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGBA8888)

        # Set the QImage to the QLabel
        pixmap = QPixmap.fromImage(qimg) 
        scaled = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(scaled)


    def switch_to_histogram(self):
        """
        Switch between displaying the histogram and the original image.
        This function is called when the "Switch to Histogram" button is clicked.
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
        Display the histogram of both input and output images.
        Args:
            zoom (int): The zoom level for the histogram. Default is 0.
        """
        self.curColorLayer = -1                                 # reset color layer index
        bgra2rgba = [2, 1, 0, 3]                                # OpenCV reads images in BGR format
        ascImgIn = np.ascontiguousarray(self.inputBGRA[:,:,bgra2rgba[self.curHistLayer]])    # convert input image to contiguous array
        ascImgOut = np.ascontiguousarray(self.outputBGRA[:,:,bgra2rgba[self.curHistLayer]])  # convert output image to contiguous array
        self.histogram_pixmap(ascImgIn, self.leftLabel, zoom)   # display histogram of input image
        self.histogram_pixmap(ascImgOut, self.rightLabel)       # no needed zoom parameter in the second call

 
    def histogram_pixmap(self, image, label, zoom=0):
        """
        Display the histogram of the given image in the specified QLabel.

        Args:
            image (numpy.ndarray): The input image as a NumPy array.
            label (QLabel): The QLabel widget where the histogram will be displayed.
            zoom (int): The zoom level for the histogram. Default is 0.
        """
        self.zoomAmount += zoom                                         # update the zoom amount if a zoom amount is passed
        fig, ax = plt.subplots()                                        # Create a new figure for the histogram
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
        
        # Overwrite the y-axis limit and ticks if the zoom amount is not 0 
        if self.zoomAmount != 0:
            zoom_factor = 1 / (1 + self.zoomAmount * 0.3)  
            yLim = round(self.yLim * zoom_factor)
            ax.set_ylim(0, yLim)
            ax.set_yticks(np.int16(np.arange(0, yLim+1, yLim / 5)))

        # set title based on the RGBA color format and current channel
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


    def switch_to_colorLayer(self):
        """
        Switch between displaying the color layers of the input and output images.
        This function is called when the "Switch to Color Layer" button is clicked.
        It allows the user to view different color channels of the images.
        The color layers are cycled through, and when the last layer is reached, it switches back to the original view.
        """
        try:
            # if the last color layer is reached, switch back to original view 
            if self.curColorLayer+1 >= 4:
                    self.curColorLayer = -1
                    # display the input and output images in the labels
                    self.image_pixmap(self.inputBGRA, self.leftLabel)  
                    self.image_pixmap(self.outputBGRA, self.rightLabel)
                    # change the text of leftTitle and rightTitle to empty string
                    self.leftTitle.setText("")
                    self.rightTitle.setText("")
            
            # else, display the next color layer
            else:
                self.curColorLayer += 1
                self.display_color_layer()  

        except Exception as e:
            QMessageBox.information(self, "Error", f"{e}")
    

    def display_color_layer(self):
        """
        Display the current color layer of both input and output images.
        It updates the displayed images in the left and right labels with the selected color channel.
        The function also resets the histogram view and zoom buttons.
        """
        self.histView = False       # reset histogram view
        self.curHistLayer = -1
        self.zoomIn.hide()          # deactivate zoom buttons
        self.zoomOut.hide()

        bgra2rgba = [2, 1, 0, 3]                                                              # OpenCV reads images in BGRA format
        ascImgIn = np.ascontiguousarray(self.inputBGRA[:,:,bgra2rgba[self.curColorLayer]])    # convert input image to contiguous array
        ascImgOut = np.ascontiguousarray(self.outputBGRA[:,:,bgra2rgba[self.curColorLayer]])  # convert output image to contiguous array
        self.image_pixmap(ascImgIn, self.leftLabel, title=True)                               # display input image
        self.image_pixmap(ascImgOut, self.rightLabel, title=True)                             # display output image


    def switch_to_frequency(self):
        """
        Switch between displaying the image and its frequency domain representation.
        This function is called when the "Switch to Frequency Domain" button is clicked.
        """
        try:
            pass
        except Exception as e:
            QMessageBox.information(self, "Error", f"{e}")


    def save_image(self, image):
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
                cv2.imwrite(filePath, image)            # Save the image using OpenCV
            except Exception as e:
                QMessageBox.information(None, "Error", f"Failed to save the image.\n{str(e)}")


