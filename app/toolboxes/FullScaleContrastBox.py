from app.toolbox_bases import DraggableToolbox
import constants
from app import processors


class FullScaleContrastBox(DraggableToolbox):
    """
    A class to create a full scale contrast adjustment toolbox.
    Adjusts the contrast of an image to full scale.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['FULL_SCALE_CONTRAST']['NAME'])
  
    def execute(self, imageBGRA, mask):
        # apply full scale contrast stretching
        imageBGRA = processors.apply_full_scale_contrast(imageBGRA, mask)  
        
        return imageBGRA
