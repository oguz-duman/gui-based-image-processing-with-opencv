from app.toolbox_bases import DraggableToolbox
import constants
from app import processors


class ThresholdingBox(DraggableToolbox):
    """
    A class to create a thresholding toolbox.
    Applies a thresholding operation to the input image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['THRESHOLDING']['NAME'])

        # insert slider to select the threshold value
        self.threshold = self.insert_slider(heading="Threshold:", minValue=0, maxValue=255, defaultValue=128)

    def execute(self, imageBGRA, mask):
        threshold = self.threshold[0].value()                               # get the threshold value from slider
        imageBGRA = processors.apply_threshold_filter(imageBGRA, threshold)          # apply thresholding
        
        return imageBGRA
