from app.toolbox_bases import DraggableToolbox
import constants
from app import processors


class BitSliceBox(DraggableToolbox):
    """
    A class to create a bit plane slicing toolbox.
    Applies bit plane slicing to the input image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['BITSLICE']['NAME'])

        # Insert a combo list to select a bit plane
        self.combo = self.insert_combo_list(["0", "1", "2", "3", "4", "5", "6", "7"])

    def execute(self, imageBGRA, mask):
        # apply bit plane slicing
        imageBGRA = processors.extract_bit_planes(imageBGRA, int(self.combo.currentText()))

        return imageBGRA

