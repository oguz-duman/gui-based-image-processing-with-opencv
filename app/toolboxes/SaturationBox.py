from app.toolbox_bases import DraggableToolbox
import constants
from app import processors

class SaturationBox(DraggableToolbox):
    """
    A class to create a saturation adjustment toolbox.
    Adjusts the saturation of an image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['SATURATION']['NAME'])

        # Create a slider to adjust saturation
        self.saturation = self.insert_slider(heading="Saturation", minValue=-50, maxValue=50)

    def execute(self, imageBGRA, mask):
        # apply saturation adjustment
        imageBGRA = processors.adjust_saturation(imageBGRA, self.saturation[0].value(), mask)     

        return imageBGRA