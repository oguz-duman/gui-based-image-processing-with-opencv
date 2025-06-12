from app.toolbox_bases import DraggableToolbox
import constants
from app import processors


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
        imageBGRA = processors.get_sobel_filter(imageBGRA, self.norm[0].isChecked())  

        return imageBGRA
