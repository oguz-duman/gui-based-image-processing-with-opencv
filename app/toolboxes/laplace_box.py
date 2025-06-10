from app.toolbox_bases import DraggableToolbox
import constants
from app import processors


class LaplaceBox(DraggableToolbox):
    """
    A class to create a laplace transformation toolbox.
    Applies a laplace transformation to the input image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['LAPLACE']['NAME'])


        # insert switch to select extended laplace and normalize options
        self.extended = self.insert_switch("Extended Laplace")
        self.norm = self.insert_switch("Normalize")

    def execute(self, imageBGRA, mask):
        # apply laplace transformation
        imageBGRA = processors.get_laplacian_filter(imageBGRA, self.extended[0].isChecked(), self.norm[0].isChecked())  

        return imageBGRA
