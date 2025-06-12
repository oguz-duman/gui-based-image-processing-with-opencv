from app.toolbox_bases import DraggableToolbox
import constants
from app import processors


class CropBox(DraggableToolbox):
    """
    A class to create a cropping toolbox.
    Crops the input image based on the specified values.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['CROP']['NAME'])

        # Insert input boxes to select the crop values
        self.leftRight  = self.insert_dual_input("Left-Right:", 0, 0)      
        self.topBottom = self.insert_dual_input("Top-Bottom:", 0, 0)
                        
    def execute(self, imageBGRA, mask):
        h,w = imageBGRA.shape[:2]       # get the height and width of the input image

        # get the crop values from input
        leftCut, rightCut = self.get_component_value(self.leftRight[:2], maxs=[w,w], defaults=[0, 0])
        topCut, bottomCut = self.get_component_value(self.topBottom[:2], maxs=[h,h], defaults=[0, 0])
        
        # apply cropping
        imageBGRA = processors.crop_image(imageBGRA, leftCut, rightCut, topCut, bottomCut)  

        return imageBGRA    
