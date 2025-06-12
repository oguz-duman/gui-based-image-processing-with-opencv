from app.toolbox_bases import DraggableToolbox
import constants
from app import processors
import numpy as np


class GammaBox(DraggableToolbox):
    """
    A class to create a gamma transformation toolbox.
    Applies a gamma transformation to an image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['GAMMA']['NAME'])

        self.slider_rescale = 10        # set a rescale factor for the slider

        # insert signle input box to select the gamma value
        self.gamma = self.insert_slider(heading="Gamma:", minValue=1, maxValue=100, defaultValue=10, rescale=self.slider_rescale)

    def execute(self, imageBGRA, mask):
        gamma = self.gamma[0].value() / self.slider_rescale             # get the threshold value from slider
        imageBGRA = processors.apply_gamma_transform(imageBGRA, gamma, mask)    # apply gamma transformation

        return np.uint8(imageBGRA)     

