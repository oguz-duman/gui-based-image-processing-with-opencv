from app.toolbox_bases import DraggableToolbox
import constants
from app import processors

class SmoothingBox(DraggableToolbox):
    """
    A class to create a smoothing toolbox.
    Applies smoothing to the input image.
    Available methods are Mean and Gaussian.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['SMOOTHING']['NAME'])

        # set rescale factor for sigma slider
        self.sigma_rescale = 10

        # insert nedded input widgets
        self.combo = self.insert_combo_list(["Mean", "Gaussian"])
        self.kernel = self.insert_mono_input("Kernel Size:", defaultValue=3)
        self.sigma = self.insert_slider(heading="Std:", minValue=1, maxValue=100, defaultValue=10, rescale=self.sigma_rescale)  

         # connect widgets to the appropriate combo lists 
        self.set_combo_adapt_widgets(self.combo, [[self.kernel], [self.kernel, self.sigma]])

    def execute(self, imageBGRA, mask):
        # get the kernel size and make sure it is odd
        w = self.get_component_value(self.kernel[:1], mins=[0], defaults=[3])         
        w = w if w % 2 == 1 else w + 1                                      
        
        # get the sigma value from inputs
        sigma = self.sigma[0].value() / self.sigma_rescale      
        
        # apply the selected smoothing method
        if self.combo.currentText() == "Mean":
            imageBGRA = processors.apply_box_filter(imageBGRA, w, mask)
        elif self.combo.currentText() == "Gaussian":
            imageBGRA = processors.apply_gaussian_blur(imageBGRA, w, sigma, mask)  

        return imageBGRA
  