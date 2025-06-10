from app.toolbox_bases import DraggableToolbox
import constants
from app import processors

class SpatialMaskBox(DraggableToolbox):
    """
    A class to create a masking toolbox.
    This toolbox allows the user to select a rectangular area of the image and apply spatial masking.
    This mask only affects the next toolbox in the pipeline not all 
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['SPATIAL_MASKING']['NAME'])

        self.im_size = [0, 0]


    def execute(self, imageBGRA, mask):

        # get the slider values and apply spatial masking
        mask = processors.generate_spatial_mask(imageBGRA, self.slid_width[0].value(), self.slid_height[0].value(),
                                                    self.slid_left[0].value(), self.slid_top[0].value(), 
                                                    self.slid_bor_radius[0].value(), self.invert[0].isChecked()) 

        return imageBGRA, mask
    
    
    def update_toolbox(self, imageBGRA):
        super().update_toolbox(imageBGRA)  

        if self.im_size == [0, 0]:
        
            # get the height and width of the image
            self.im_size = [0, 0] if self.imageBGRA is None else self.imageBGRA.shape[:2]  

            # insert a switch to invert the mask
            self.invert = self.insert_switch("Invert the mask")
            
            # insert sliders for width, height, left position, top position and border radius
            self.slid_width = self.insert_slider(heading="Width:", minValue=1, maxValue=self.im_size[1], defaultValue=self.im_size[1])
            self.slid_height = self.insert_slider(heading="Height:", minValue=1, maxValue=self.im_size[0], defaultValue=self.im_size[0])
            self.slid_left = self.insert_slider(heading="Left:", minValue=0, maxValue=self.im_size[1], defaultValue=0)
            self.slid_top = self.insert_slider(heading="Top:", minValue=0, maxValue=self.im_size[0], defaultValue=0)
            self.slid_bor_radius = self.insert_slider(heading="Border Radius:", minValue=0, maxValue=100, defaultValue=0) 
 