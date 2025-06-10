from app.toolbox_bases import DraggableToolbox
import constants
from app import processors

class ContrastBox(DraggableToolbox):
    """
    A class to create a contrast adjustment toolbox.
    Adjusts the contrast of an image.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['CONTRAST']['NAME'])

        self.slider_rescale = 10    # set a rescale factor for the slider

        # insert a combo list to select between input type (range or T(s))
        self.combo = self.insert_combo_list(["by Input-Output Range", "by T(s)"])

        # insert min-max input boxes for input and output range
        self.inMinMax = self.insert_dual_input("Input Range:")
        self.outMinMax = self.insert_dual_input("Output Range:")

        # insert sliders for alpha and beta values
        self.alpha = self.insert_slider(heading="Alpha:", minValue=1, maxValue=30, defaultValue=10, rescale=self.slider_rescale)
        self.beta = self.insert_slider(heading="Beta:", minValue=-50, maxValue=50)  

        # connect widgets to the appropriate combo lists  
        self.set_combo_adapt_widgets(self.combo, [[self.inMinMax, self.outMinMax], [self.alpha, self.beta]])

    def execute(self, imageBGRA, mask):

        if self.combo.currentText() == "by Input-Output Range":
            # get input and output range values from the text boxes
            in_min, in_max = self.get_component_value(self.inMinMax[:2], maxs=[255,255], defaults=[0, 255])
            out_min, out_max = self.get_component_value(self.outMinMax[:2], maxs=[255,255], defaults=[0, 255])

            # apply contrast stretching using input-output range method
            imageBGRA = processors.adjust_contrast_by_range(imageBGRA, [in_min, in_max], [out_min, out_max], mask)  

            return imageBGRA  

        elif self.combo.currentText() == "by T(s)":
            # get the alpha and beta values from sliders
            alpha = self.alpha[0].value() / self.slider_rescale
            beta = self.beta[0].value()

            # apply contrast stretching using T(s) method
            imageBGRA = self.adjust_contrast_by_T(imageBGRA, alpha, beta, mask)  
            
            return imageBGRA
              