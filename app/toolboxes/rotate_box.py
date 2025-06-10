from app.toolbox_bases import DraggableToolbox
import constants
from app import processors


class RotateBox(DraggableToolbox):
    """
    A class to create a rotation toolbox.
    Rotates the input image based on the selected angle.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['ROTATE']['NAME'])

        # Insert a slider to adjust the rotate angle
        self.angle = self.insert_slider(heading="Angle: ", minValue=-180, maxValue=180)  

    def execute(self, imageBGRA, mask):
        value = self.angle[0].value()                           # Get the current value of the slider
        imageBGRA = processors.rotate_image(imageBGRA, value)         # Apply rotation

        return imageBGRA
