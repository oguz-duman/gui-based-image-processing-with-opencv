from app.toolbox_bases import DraggableToolbox
import constants
from app import processors
import cv2

class ResizeBox(DraggableToolbox):
    """
    A class to create a resizing toolbox.
    Resizes the input image based on the specified width and height.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['RESIZE']['NAME'])

        self.im_width = 0
        self.im_height = 0
                        
    def execute(self, imageBGRA, mask):

        if self.combo.currentText() == "Resize by Absolute Size":
            # get input and output range values from the text boxes
            reWidth, reHeight = self.get_component_value(self.newWidthHeight[:2], mins=[0, 0], defaults=[self.im_width, self.im_height])
        elif self.combo.currentText() == "Resize by Percentage":
            # get the percentage value from the slider and calculate the new width and height
            percentage = self.percentage[0].value() / 100
            reWidth = int(self.im_width * percentage)
            reHeight = int(self.im_height * percentage)
            
        # apply resizing
        imageBGRA = processors.resize_image(imageBGRA, reWidth, reHeight, self.interpolation_types[self.interpolation.currentIndex()])  
    
        return imageBGRA


    def update_toolbox(self, imageBGRA):
        """
        Runs only when the toolbox is created for the first time and everytime the input image is changed. 
        """
        super().update_toolbox(imageBGRA)

        if [self.im_width, self.im_height] == [0, 0]:
            
            # insert a combo list to select between resize by absolute size and by percentage
            self.combo = self.insert_combo_list(["Resize by Absolute Size", "Resize by Percentage"])

            # insert a slider to select the percentage value
            self.percentage = self.insert_slider(heading="Percentage:", minValue=1, maxValue=100, defaultValue=100)

            # Insert min-max input boxes to select the new size
            self.newWidthHeight  = self.insert_dual_input("Size:", 0, 0)

            # order of the interpolation types in this list must be in the same order as in self.interpolation_types
            self.interpolation = self.insert_combo_list(["None", "INTER_NEAREST", "INTER_LINEAR", "INTER_AREA", "INTER_CUBIC",
                                                        "INTER_LANCZOS4", "INTER_LINEAR_EXACT"])
            
            self.interpolation_types = [None, cv2.INTER_NEAREST, cv2.INTER_LINEAR, cv2.INTER_AREA, cv2.INTER_CUBIC,
                                        cv2.INTER_LANCZOS4, cv2.INTER_LINEAR_EXACT]
            
            # connect widgets to the appropriate combo lists
            self.set_combo_adapt_widgets(self.combo, [[self.newWidthHeight], [self.percentage]])
            
            # get the height and width of the image
            self.im_width, self.im_height = [128, 128] if self.imageBGRA is None else self.imageBGRA.shape[:2]  

            # set the input boxes to the image size as default
            self.newWidthHeight[0].setText(str(self.im_height))
            self.newWidthHeight[1].setText(str(self.im_width))
 