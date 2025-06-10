from app.toolbox_bases import DraggableToolbox
import constants
from app import processors


class HistEqualizationBox(DraggableToolbox):
    """
    A class to create a histogram equalization toolbox.
    Applies histogram equalization to the input image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['HISTEQ']['NAME'])
  
    def execute(self, imageBGRA, mask):
        # apply histogram equalization
        imageBGRA = processors.apply_histogram_equalization(imageBGRA, mask)  
        
        return imageBGRA
