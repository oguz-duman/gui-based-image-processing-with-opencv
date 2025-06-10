from app.toolbox_bases import DraggableToolbox
import constants
from app import processors


class HistCLAHEBox(DraggableToolbox):
    """
    A class to create a histogram CLAHE toolbox.
    Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) to the input image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['HISTCLAHE']['NAME'])

        self.clipLimit_rescale = 10     # set a rescale factor for the slider

        # Insert a slider and input box to select the clip limit and tile grid size
        self.clipLimit = self.insert_slider(heading="Clip Limit:", minValue=1, maxValue=100, defaultValue=2, rescale=self.clipLimit_rescale)  
        self.tileGridSize = self.insert_mono_input("Tile Grid Size:", defaultValue=8)

    def execute(self, imageBGRA, mask):
        # get the clip limit and tile grid size values
        clipLimit = self.clipLimit[0].value() / self.clipLimit_rescale
        tileGridSize = self.get_component_value(self.tileGridSize[:1], mins=[4], maxs=[64], defaults=[8])
        tileGridSize = tileGridSize if tileGridSize % 2 == 0 else tileGridSize + 1          # allow only even numbers for tile grid size

        # apply CLAHE
        imageBGRA = processors.apply_clahe(imageBGRA, clipLimit, tileGridSize, mask)

        return imageBGRA
 