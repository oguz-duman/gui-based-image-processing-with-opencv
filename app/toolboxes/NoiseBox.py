from app.toolbox_bases import DraggableToolbox
import constants
from app import processors


class NoiseBox(DraggableToolbox):
    """
    A class to create a noise toolbox.
    Applies different types of noises to the input image.
    Available noise types are Gaussian, Salt & Pepper, and Poisson.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['ADD_NOISE']['NAME'])

        self.saltPepProb_rescale = 1000         # set a rescale factor for the slider

        # Insert a combo list to select the noise type
        self.combo = self.insert_combo_list(["Gaussian", "Salt & Pepper", "Poisson"])

        # insert signle input boxes to select the mean and std values
        self.mean = self.insert_slider(heading="Mean:", minValue=-30, maxValue=300, defaultValue=0)
        self.std = self.insert_slider(heading="Std:", minValue=0, maxValue=100, defaultValue=25)

        # insert signle input boxes to select the salt and pepper probability
        self.saltPepProb = self.insert_slider(heading="Probability:", minValue=0, maxValue=200, defaultValue=20, rescale=self.saltPepProb_rescale)

         # connect widgets to the appropriate combo lists 
        self.set_combo_adapt_widgets(self.combo, [[self.mean, self.std], [self.saltPepProb], []])
   
    def execute(self, imageBGRA, mask):
        if self.combo.currentText() == "Gaussian":
            # get mean and std values from inputs and apply gaussian noise
            mean = self.mean[0].value() 
            std = self.std[0].value()
            imageBGRA = processors.add_gaussian_noise(imageBGRA, mean, std, mask)  
            
            return imageBGRA
        
        elif self.combo.currentText() == "Salt & Pepper":
            # get salt and pepper probability values from the text boxes and apply salt and pepper noise
            saltPepProb = self.saltPepProb[0].value() / self.saltPepProb_rescale
            imageBGRA = self.add_salt_and_pepper(imageBGRA, saltPepProb, mask)
            
            return imageBGRA    
        
        elif self.combo.currentText() == "Poisson": 
            # apply poisson noise
            imageBGRA = self.add_poisson_noise(imageBGRA, mask)
            
            return imageBGRA
  