from app.toolbox_bases import DraggableToolbox
import constants
from app import processors
import numpy as np


class ColorMaskBox(DraggableToolbox):
    """
    A class to create a masking toolbox.
    This toolbox allows the user to select a range of HSV values to create a mask.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['COLOR_MASKING']['NAME'])

        # Insert a switch to invert the mask
        self.invert = self.insert_switch("Invert the mask")

        # Insert input boxes to select the min-max HSV values
        self.intensityMin = self.insert_triple_input("min HSV:", 0, 0, 0)
        self.intensityMax = self.insert_triple_input("max HSV:", 0, 0, 0)

    def execute(self, imageBGRA, mask):
        # get the min-max HSV values from the input boxes
        rMin, gMin, bMin = self.get_component_value(self.intensityMin[:3], mins=[0, 0, 0], maxs=[255,255, 255], defaults=[0, 0, 0])
        rMax, gMax, bMax = self.get_component_value(self.intensityMax[:3], mins=[0, 0, 0], maxs=[255,255, 255], defaults=[0, 0, 0])

        # apply masking
        mask = processors.generate_color_mask(imageBGRA, np.asarray([rMin, gMin, bMin]), np.asarray([rMax, gMax, bMax]), self.invert[0].isChecked())

        return imageBGRA, mask
  