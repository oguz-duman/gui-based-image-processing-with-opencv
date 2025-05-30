import cv2
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

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

    def init_ui_variables(self, toolbox_wrapper, footer_toolbox, in_im_canvas, out_im_canvas):
        """
        Gets the necessary widgets and layout from the 'main_window' and sets up the pipeline.
        Args:
            toolbox_wrapper (QVBoxLayout): The layout where the toolboxes are added.
            footer_toolbox (QWidget): The footer widget for the toolbox layout.
            in_im_canvas (MatplotlibCanvas): The canvas for displaying the input image.
            out_im_canvas (MatplotlibCanvas): The canvas for displaying the output image.
        """
        self.toolbox_wrapper = toolbox_wrapper
        self.footer_toolbox = footer_toolbox
        self.in_im_canvas = in_im_canvas
        self.out_im_canvas = out_im_canvas

        # Initialize the pipeline
        self.pipeline = Pipeline()  

        # Modes and their corresponding methods which are called when the mode is activated
        self.mode_handlers = {      
            'IMAGE': lambda: self.display_images([self.input_BGRA, self.output_BGRA]),  
            'HISTOGRAM': lambda: self.display_histogram(),
            'CHANNELS': lambda: self.display_images(self.get_color_channels()),  
            'FREQUENCY': lambda: self.display_images(self.fourier_transform())
        }


    def init_variables(self):
        """
        Initialize the variables used in the ui.
        """
        self.input_BGRA = None                      # input image variable
        self.output_BGRA = None                     # output image variable
        
        self.active_mode = 'IMAGE'                  # current mode mode variable
        self.channel_index = 0                      # current color layer variable
        
        
    def open_new_image(self):
        """
        This method is called when the 'Open Image' button is clicked.
        It opens a file dialog to select an image file, reads the image using OpenCV, and displays it in the UI.
        """
        image = self.select_image()              # select an image using the file dialog

        if image is not None:
            self.init_variables()                # reinitialize variables since a new image is opened

            self.input_BGRA = image.copy()       # make a copy of the input image for input
            self.output_BGRA = image.copy()      # make a copy of the input image for output

            # display the input and output images in the labels
            self.display_images([self.input_BGRA, self.output_BGRA])  

            self.pipeline_on_change()            # process the image through the pipeline

            # update toolbox components according to new image (max slider values, etc.)
            for toolbox in self.pipeline.steps:  
                toolbox.update_toolbox(self.input_BGRA)



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
    def insert_toolbox(self, toolbox_name):
        """
        Add a new toolbox to the layout and pipeline.
        Args:
            toolbox_name (str): The name of the method to be added.
        """
        # Create a new method box based on the selected method name
        for toolbox in constants.TOOLBOXES.values():
            if toolbox_name == toolbox['NAME']:
                toolbox_class = getattr(toolboxes, toolbox['CLASS'])
                new_toolbox = toolbox_class()  # create an instance of the toolbox class
                break

        # connect the toolbox signals
        new_toolbox.updateTrigger.connect(self.pipeline_on_change)   
        new_toolbox.removeTrigger.connect(self.remove_toolbox) 

        new_toolbox.update_toolbox(self.input_BGRA)                 # update the toolbox with the input image

        self.pipeline.add_step(new_toolbox)                         # add the toolbox to the pipeline

        self.toolbox_wrapper.removeWidget(self.footer_toolbox)      # remove the special footer widget
        self.footer_toolbox.setParent(None)           
        self.toolbox_wrapper.addWidget(new_toolbox)                 # add the toolbox to the layout
        self.toolbox_wrapper.addWidget(self.footer_toolbox)         # add the special footer widget back

        self.pipeline_on_change()                                   # trigger the update method to rerun the updated pipeline 


    @Slot(str)
    def remove_toolbox(self, id):
        """
        Remove the toolbox from layout and pipeline.
        Args:
            toolbox (str): The name of the toolbox to be removed.
        """
        # remove the toolbox from the layout
        for i in range(self.toolbox_wrapper.count()):
            widget = self.toolbox_wrapper.itemAt(i).widget()
            if widget and widget.id == id:
                self.toolbox_wrapper.removeWidget(widget)
                widget.setParent(None)
                break
        
        self.pipeline.remove_step(id)               # remove toolbox from the pipeline
        self.pipeline_on_change()                   # rerun the pipeline
   

    def pipeline_on_change(self):
        """
        This method is called when the pipeline is updated.
        It runs the pipeline on the input image and updates the ui based on the current mode.
        """
        if self.input_BGRA is not None:
            self.output_BGRA = self.pipeline.run(self.input_BGRA)               # run the pipeline on the input image
            self.mode_handlers[self.active_mode]()                              # update the ui based on the current mode

          
    def mode_buttons(self, mode_name):
        """
        Handles mode button clicks: switches to a new mode if needed,
        or cycles within the current mode if applicable.
        Args:
            mode_name (str): The name of the mode that was selected.
        """
        if self.input_BGRA is None:
            return
        elif not self.active_mode == mode_name:
            self.switch_mode(mode_name)   
            self.mode_handlers[mode_name]()             # call the method corresponding to the mode name             
        else:
            self.channel_index = self.channel_index + 1 if self.channel_index + 1 < len(CHANNEL_NAMES) else 0  # increment the channel index 
            if self.channel_index == 0:
                self.switch_mode('IMAGE')  
                self.display_images([self.input_BGRA, self.output_BGRA])
            else:
                self.mode_handlers[mode_name]()          # call the method corresponding to the mode name             


    def switch_mode(self, mode_name):
        """
        Updates the active mode and toggles visibility of related UI widgets.
        Args:
            mode_name (str): The name of the mode to switch to.
        """
        self.active_mode = mode_name                # active mode name
        self.channel_index = 0                      # reset channel index


    def display_images(self, images):
        """
        Display input and output images on the embedded matplotlib canvas.

        Parameters:
            images (list): A list containing the images to be displayed. 
        """
        for image, canvas in zip(images, [self.in_im_canvas, self.out_im_canvas]):
            
            # clear the current canvas and plot the new image
            canvas._axes.clear()                             
            canvas._axes.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # Set the axes properties
            canvas._axes.set_title("Image View", fontsize=10)
            canvas._axes.axis('off')  
            canvas.draw()

            canvas._orig_xlim = canvas._axes.get_xlim()
            canvas._orig_ylim = canvas._axes.get_ylim()

 
    def display_histogram(self):
        """
        Plot the histogram of the given image on the canvas.
        Args:
            image (numpy.ndarray): The image data for which the histogram is to be plotted.
        """
        for image, canvas in zip([self.input_BGRA, self.output_BGRA], [self.in_im_canvas, self.out_im_canvas]):

            canvas._axes.clear()                    # clear the current canvas                         
            bgra2rgba = [2, 1, 0, 3]                # OpenCV uses BGRA format, convert to RGBA for display
            canvas._axes.hist(self.output_BGRA[:, :, bgra2rgba[self.channel_index]].ravel(), bins=256, alpha=0.5)

            canvas._axes.set_title('Histogram')
            canvas._axes.set_xlim(left=0, right=256)
            canvas.draw()


    def get_color_channels(self):
        """
        Get the currently active color channel from the input and output images.
        Returns:
            list: A list containing the currently active color channel from the input and output images.
        """
        # OpenCV handles images in BGRA format. Convert RGBA indeces to BGRA.
        bgra2rgba = [2, 1, 0, 3]    

        return [
            self.input_BGRA[:,:,bgra2rgba[self.channel_index]], 
            self.output_BGRA[:,:,bgra2rgba[self.channel_index]]
        ]                    


    def fourier_transform(self):
        """
        Perform a Fourier Transform on the input image and return the magnitude spectrum.
        Returns:
            list: A list containing the magnitude spectrum of the Fourier Transform of the input and output images.
        """
        bgra2rgba = [2, 1, 0, 3]   
        magnitude_spectrums = []  

        for image in [self.input_BGRA, self.output_BGRA]:
            ch_float = np.float32(image[:,:,bgra2rgba[self.channel_index]])
            dft = cv2.dft(ch_float, flags=cv2.DFT_COMPLEX_OUTPUT)
            dft_shift = np.fft.fftshift(dft)
            magnitude = cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1])
            magnitude_log = np.log(magnitude + 1)
            magnitude_norm = cv2.normalize(magnitude_log, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            magnitude_bgra = cv2.cvtColor(magnitude_norm, cv2.COLOR_GRAY2BGRA)
            magnitude_spectrums.append(magnitude_bgra)

        return magnitude_spectrums


    def save_image(self):
        """
        Open a file dialog to select a file path to save the output image.
        """
        # Open file dialog to select a file path to save the image
        filePath, _ = QFileDialog.getSaveFileName(None, "Save the image", "", "Image Files (*.jpg *.jpeg *.png *.bmp *.gif *.tif *.tiff *.webp)")
        
        # Check if a file path was selected
        if filePath:
            try:
                cv2.imwrite(filePath, self.output_BGRA)            # Save the image using OpenCV
            except Exception as e:
                QMessageBox.information(None, "Error", f"Failed to save the image.\n{str(e)}")


