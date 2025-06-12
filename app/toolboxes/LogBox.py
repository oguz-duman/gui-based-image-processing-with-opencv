from app.toolbox_bases import DraggableToolbox
import constants
from app import processors

class LogBox(DraggableToolbox):
    """
    A class to create a log transformation toolbox.
    Applies a logarithmic transformation to an image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['LOG']['NAME'])
          
    def execute(self, imageBGRA, mask):
        # apply log transformation
        imageBGRA = processors.apply_log_transform(imageBGRA, mask)  

        return imageBGRA

