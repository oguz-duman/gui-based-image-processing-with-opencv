from app.toolbox_bases import DraggableToolbox
import constants
from app import processors

class BrightnessBox(DraggableToolbox):
    """
    A class to create a brightness adjustment toolbox.
    Adjusts the brightness of an image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['BRIGHTNESS']['NAME'])

        # create a combo box to select the color channel which the brightness cahnge will be applied to
        self.color_channel = self.insert_combo_list(["HSV", "RGB"])
            
        # Create a slider to adjust brightness
        self.brightness = self.insert_slider(heading="Brightness", minValue=-100, maxValue=100)  

    def execute(self, imageBGRA, mask):
        # apply brightness adjustment
        imageBGRA = processors.adjust_brightness(imageBGRA, self.brightness[0].value(), self.color_channel.currentText(), mask)  

        return imageBGRA