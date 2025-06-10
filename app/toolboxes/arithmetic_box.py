from app.toolbox_bases import DraggableToolbox
import constants
from app import processors
from app.toolbox_bases import select_image
import cv2

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
            imageBGRA = processors.apply_image_arithmetic(imageBGRA, self.secondImage, alpha, operation)  # apply arithmetic operation

        return imageBGRA
    
    def open_second_image_button(self):
        """
        Open a file dialog to select the second image.
        """
        imageBGRA = select_image(None)     # read the image

        if imageBGRA is not None:
            self.secondImage = cv2.cvtColor(imageBGRA, cv2.COLOR_BGRA2BGR)  # convert the image to BGR format
            self.updateTrigger.emit()        # emit the signal to indicate that the settings have been changed
