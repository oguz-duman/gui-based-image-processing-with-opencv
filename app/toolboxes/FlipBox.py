from app.toolbox_bases import DraggableToolbox
import constants
from app import processors



class FlipBox(DraggableToolbox):
    """
    A class to create a flipping toolbox.
    Flips the input image based on the selected direction.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['FLIP']['NAME'])

        # Insert a radio button group to select the flip direction
        self.buttonGroup = self.insert_radio_buttons(["Horizontal", "Vertical", "Both"])

    def execute(self, imageBGRA, mask):
        flipCodes = [1, 0, -1]          # horizontal, vertical, both
        imageBGRA = processors.flip_image(imageBGRA, flipCodes[self.buttonGroup[0].checkedId()])  # apply flipping

        return imageBGRA
    
