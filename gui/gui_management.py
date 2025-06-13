import cv2
import numpy as np

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMessageBox, QFileDialog

import constants
from constants import VISUALIZATION_TYPES
from app.pipeline import Pipeline
from app import toolboxes


class GUiManagement():
    """
    This class manages the UI elements and interactions for the image processing application.
    It handles image loading, toolbox insertion and deletion, histogram display, color layer switching, image saving and displaying.
    """
    def __init__(self):
        self.init_variables()

    def init_ui_variables(self, toolbox_wrapper, footer_toolbox, in_im_canvas, out_im_canvas, 
                          left_title, right_title, vis_mod_list, color_chan_list):
        """
        Gets the necessary widgets and layout from the 'main_window' and sets up the pipeline.
        Args:
            toolbox_wrapper (QVBoxLayout): The layout where the toolboxes are added.
            footer_toolbox (QWidget): The footer widget for the toolbox layout.
            in_im_canvas (MatplotlibCanvas): The canvas for displaying the input image.
            out_im_canvas (MatplotlibCanvas): The canvas for displaying the output image.
            left_title (QLabel): The label for the left title.
            right_title (QLabel): The label for the right title.
        """
        self.toolbox_wrapper = toolbox_wrapper
        self.footer_toolbox = footer_toolbox
        self.in_im_canvas = in_im_canvas
        self.out_im_canvas = out_im_canvas
        self.left_title = left_title
        self.right_title = right_title
        self.vis_mod_list = vis_mod_list
        self.color_chan_list = color_chan_list

        # Initialize the pipeline
        self.pipeline = Pipeline()  

        # Modes and their corresponding methods which are called when the mode is activated. Watch the order of the methods in the list.
        self.view_handlers = {      
            list(VISUALIZATION_TYPES.keys())[0]: lambda: self.display_images(self.get_color_channels()),  
            list(VISUALIZATION_TYPES.keys())[1]: lambda: self.display_histogram(),
            list(VISUALIZATION_TYPES.keys())[2]: lambda: self.display_images(self.fourier_transform())
        }

        # Declares which widgets will be shown and which widgets will be hidden based on the selected mode. Watch the order of the methods in the list.
        self.widgets_per_mode = {
            list(VISUALIZATION_TYPES.keys())[0]: [self.left_title, self.right_title],
            list(VISUALIZATION_TYPES.keys())[1]: [],
            list(VISUALIZATION_TYPES.keys())[2]: [self.left_title, self.right_title]
        }


    def init_variables(self):
        """
        Initialize the variables used in the ui.
        """
        self.input_BGRA = None                      # input image variable
        self.output_BGRA = None                     # output image variable
        self.view_mode = "Image"                    # name of the currently active view mode
        self.color_channel = "RGBA"            # name of the currently active color channel   

    def open_new_image(self):
        """
        This method is called when the 'Open Image' button is clicked.
        It opens a file dialog to select an image file, reads the image using OpenCV, and displays it in the UI.
        """
        image = self.select_image()              # select an image using the file dialog

        if image is not None:
            self.init_variables()                # reinitialize all the variables
            
            self.input_BGRA = image.copy()       # make a copy of the input image for input
            self.output_BGRA = image.copy()      # make a copy of the input image for output

            # update toolbox components according to new image (max slider values, etc.)
            for toolbox in self.pipeline.steps:  
                toolbox.update_toolbox(self.input_BGRA)

            self.vis_mod_list.setCurrentIndex(0)        # reset the view mode and color channel lists.
            self.pipeline_on_change()                   # process the image through the pipeline


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
            self.view_handlers[self.view_mode]()                                # update the ui based on the current mode



    def switch_view(self, mode_name):
        """
        Switch the view mode to the specified mode and update the UI accordingly.
        Args:
            mode_name (str): The name of the mode to switch to.
        """
        if self.input_BGRA is None:
            return
        
        # Reset the x and y limits (zooming) for the input and output image canvases
        for canvas in [self.in_im_canvas, self.out_im_canvas]:
            canvas._xlim = 0
            canvas._ylim = 0

        # show or hide the relevant widgets based on the selected mode
        widgets_to_show = []
        for w in self.widgets_per_mode.keys():
            if w == mode_name:
                for widget in self.widgets_per_mode[w]:
                    widgets_to_show.append(widget)
            else:
                for widget in self.widgets_per_mode[w]:
                    widget.hide()

        for widget in widgets_to_show:
            widget.show()

        # Update the view mode and color channel variables
        self.view_mode = mode_name                  
        self.color_channel = VISUALIZATION_TYPES[mode_name][0].split(" ")[0]                   

        # Clear existing color channels and add new ones based on selected mode
        self.color_chan_list.blockSignals(True)
        self.color_chan_list.clear()
        self.color_chan_list.blockSignals(False)
        self.color_chan_list.addItems(VISUALIZATION_TYPES[mode_name])  # This will trigger the switch_color_chan method and update the view


    def switch_color_chan(self, channel_name):
        """
        Switch the color channel to the specified channel and update the UI accordingly.
        Args:
            channel_name (str): The name of the color channel to switch to.
        """
        if self.input_BGRA is None:
            return
        
        self.color_channel = channel_name.split(" ")[0]     # get the color channel name from the button text
        self.view_handlers[self.view_mode]()                # update the view based on the current view mode


    def display_images(self, images):
        """
        Display input and output images on the embedded matplotlib canvas.

        Parameters:
            images (list): A list containing the images to be displayed. 
        """
        # Toggle visibility of titles based on the color channel
        if self.color_channel == "RGBA":
            self.left_title.hide()
            self.right_title.hide()
        else:
            self.left_title.show()
            self.right_title.show()
            self.left_title.setText(f"{self.color_channel} Channel")
            self.right_title.setText(f"{self.color_channel} Channel")

        # Convert the images to BGRA format if they are 1-channel grayscale images
        for i in range(len(images)):
            if len(images[i].shape) == 2:
                images[i] = cv2.cvtColor(images[i], cv2.COLOR_GRAY2BGRA)

        # Plot the images on the respective canvases
        for image, canvas in zip(images, [self.in_im_canvas, self.out_im_canvas]):
            
            # clear the current canvas and plot the new image
            canvas._axes.clear()                             
            canvas._axes.imshow(image[:, :, [2, 1, 0, 3]], interpolation="none")    # convert BGRA to RGBA and display it
            canvas.configuration_types("image")
            canvas.draw()

            # get original x and y limits to limit zooming and panning
            canvas._orig_xlim = canvas._axes.get_xlim()
            canvas._orig_ylim = canvas._axes.get_ylim()

            # set the x and y limits to the previous values if any
            if canvas._xlim and canvas._ylim:
                canvas._axes.set_xlim(canvas._xlim)
                canvas._axes.set_ylim(canvas._ylim)
                canvas.draw()
 

    def display_histogram(self):
        """
        Plot the histogram of the given image on the canvas.
        """ 
        y_lims = []  
        canvases = [self.in_im_canvas, self.out_im_canvas] 
        for image, canvas in zip(self.get_color_channels(), [self.in_im_canvas, self.out_im_canvas]):
            canvas._axes.clear()
            
            # image can be in the form of 1-channel grayscale or 4-channel BGRA
            channel_count = image.shape[2] if len(image.shape) == 3 else 1
            # plot the histogram for each channel if the image has more than 1 channel
            for i in range(channel_count):
                channel = image if channel_count == 1 else image[:, :, i]       

                # Calculate histogram values and bin edges
                hist_vals, bin_edges = np.histogram(channel, bins=255, range=(0, 256))

                # Use midpoints for x-axis
                bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
                
                # Set the color for the histogram
                if self.color_channel == "RGBA":
                    colors = ['blue', 'green', 'red', 'black']
                elif self.color_channel == "Red" or self.color_channel == "Green" or self.color_channel == "Blue":
                    colors = [self.color_channel]
                else:
                    colors = ['black']

                # Plot as step plot
                canvas._axes.step(bin_centers, hist_vals, color=colors[i], where='mid', linewidth=1)
                
                # Get the maximum y value for setting the y-axis limit 
                y_lims.append(np.max(hist_vals) * 1.1)               
                
                # Set style and labels
                canvas._axes.set_xlim(-1, 256)
                canvas._axes.set_xticks(np.append(np.arange(0, 250, 25), 255))
                canvas.configuration_types("histogram")
                canvas._axes.set_title(f"{self.color_channel} Channel")
                canvas.figure.tight_layout()  

                # Calculate the y-axis limit for both histograms
                y_lim = np.max(y_lims)                          
                yStep = y_lim / 5     

        # Set the y-axis limits and ticks for both histograms and draw the canvases
        for _canvas in canvases:
            _canvas._axes.set_ylim(0, y_lim)                   
            _canvas._axes.set_yticks(np.uint32(np.arange(0, y_lim+1, yStep)))
    
            _canvas.draw()


    def get_color_channels(self):
        """
        Extracts the specified color channel from the input and output images.
        Returns:
            list: A list containing the extracted color channels from the input and output images.
        """
        channel_maps = {
            "Red":       ("BGR", 2),
            "Green":     ("BGR", 1),
            "Blue":      ("BGR", 0),
            "Alpha":     ("BGR", 3),
            "Hue":       ("HSV", 0),
            "Saturation":("HSV", 1),
            "Value":     ("HSV", 2),
            "Lightness": ("LAB", 0),
            "Green-Red": ("LAB", 1),
            "Blue-Yellow":("LAB", 2)
        }

        # If the color channel is not specified or is RGBA, return the input and output images as they are (4 channel BGRA images)
        if self.color_channel not in channel_maps or self.color_channel == "RGBA":
            return [self.input_BGRA, self.output_BGRA]

        space, index = channel_maps[self.color_channel]

        def extract_channel(image, space, index):
            if space == "BGR":
                channel = image[:, :, index]
            else:
                converted = cv2.cvtColor(image[:, :, :3], getattr(cv2, f'COLOR_BGR2{space}'))
                channel = converted[:, :, index]
            return channel

        # Return the extracted channels (1 channel grayscale images)
        return [
            extract_channel(self.input_BGRA, space, index),
            extract_channel(self.output_BGRA, space, index)
        ]


    def fourier_transform(self):
        """
        Perform a Fourier Transform on the input image and return the magnitude spectrum.
        Returns:
            list: A list containing the magnitude spectrum of the Fourier Transform of the input and output images.
        """
        magnitude_spectrums = []  

        for channel in self.get_color_channels():
            
            ch_float = np.float32(channel)         # convert the channel to float32   
            dft = cv2.dft(ch_float, flags=cv2.DFT_COMPLEX_OUTPUT)
            dft_shift = np.fft.fftshift(dft)
            magnitude = cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1])
            magnitude_log = np.log(magnitude + 1)
            magnitude_norm = cv2.normalize(magnitude_log, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            mag_im = cv2.cvtColor(magnitude_norm, cv2.COLOR_GRAY2BGRA)  
            magnitude_spectrums.append(mag_im)

        return magnitude_spectrums


    def save_image(self):
        """
        Open a file dialog to select a file path to save the output image.
        """
        # Open file dialog to select a file path to save the image
        filePath, _ = QFileDialog.getSaveFileName(None, "Save the image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp)")
        
        # Check if a file path was selected
        if filePath:
            try:
                cv2.imwrite(filePath, self.output_BGRA)            # Save the image using OpenCV
            except Exception as e:
                QMessageBox.information(None, "Error", f"Failed to save the image.\n{str(e)}")


