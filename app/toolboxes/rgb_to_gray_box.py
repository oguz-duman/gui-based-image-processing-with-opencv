from app.toolbox_bases import DraggableToolbox
import constants
from app import processors


class RGB2GrayBox(DraggableToolbox):
    """
    A class to create a RGB to grayscale conversion toolbox.
    Converts the input image to grayscale.
    Works even if the input image is already grayscale.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['RGB2GRAY']['NAME'])

    def execute(self, imageBGRA, mask):
        # apply RGB to grayscale conversion
        imageBGRA = processors.apply_rgb2gray_transform(imageBGRA)              

        return imageBGRA
