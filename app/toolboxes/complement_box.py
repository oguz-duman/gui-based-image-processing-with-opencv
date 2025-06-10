from app.toolbox_bases import DraggableToolbox
import constants
from app import processors


class ComplementBox(DraggableToolbox):
    """
    A class to create a complement toolbox.
    Applies a complement operation to the input image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['COMPLEMENT']['NAME'])
  
    def execute(self, imageBGRA, mask):
        imageBGRA = processors.get_image_complement(imageBGRA)    # apply complement operation

        return imageBGRA
