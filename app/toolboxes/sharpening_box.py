from app.toolbox_bases import DraggableToolbox
import constants
from app import processors


class SharpeningBox(DraggableToolbox):
    """
    A class to create a sharpening toolbox.
    Applies sharpening to the input image.
    Available methods are Laplace, Sobel, and Unsharp Masking.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['SHARPENING']['NAME'])

        # set rescale factors for sliders
        self.alpha_rescale = 100
        self.sigma_rescale = 10

        # insert nedded input widgets
        self.combo = self.insert_combo_list(["Laplace Sharpening", "Sobel Sharpening", "Unsharp Masking"])
        self.kernel = self.insert_mono_input("Kernel Size:", defaultValue=3)
        self.sigma = self.insert_slider(heading="Std:", minValue=1, maxValue=100, defaultValue=10, rescale=self.sigma_rescale)  
        self.extended = self.insert_switch("Extended Laplace")
        self.alpha = self.insert_slider(heading="Alpha:", minValue=1, maxValue=1000, defaultValue=100, rescale=self.alpha_rescale)

         # connect widgets to the appropriate combo lists 
        self.set_combo_adapt_widgets(self.combo, [[self.extended, self.alpha], [self.alpha],
                                                                 [self.kernel, self.sigma, self.alpha]])

    def execute(self, imageBGRA, mask):
        # get the kernel size and make sure it is odd
        w = self.get_component_value(self.kernel[:1], mins=[0], defaults=[3])         
        w = w if w % 2 == 1 else w + 1                                      
        
        # get the sigma, alpha and extended laplace values from inputs
        sigma = self.sigma[0].value() / self.sigma_rescale      
        alpha = self.alpha[0].value() / self.alpha_rescale      
        extended = self.extended[0].isChecked()                 
        
        # apply the selected sharpening method
        if self.combo.currentText() == "Laplace Sharpening":
            imageBGRA = processors.apply_laplacian_sharpening(imageBGRA, alpha, extended, mask)
        elif self.combo.currentText() == "Sobel Sharpening":
            imageBGRA = processors.apply_sobel_sharpening(imageBGRA, alpha, mask)
        elif self.combo.currentText() == "Unsharp Masking":
            imageBGRA = processors.apply_unsharp_mask(imageBGRA, w, sigma, alpha, mask)

        return imageBGRA
 