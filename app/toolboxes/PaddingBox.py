from app.toolbox_bases import DraggableToolbox
import constants
from app import processors
import cv2

class PaddingBox(DraggableToolbox):
    """
    A class to create a padding toolbox.
    Applies padding to the input image based on the selected type and values.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['PADDING']['NAME'])

        # Insert a combo list to select the padding type
        self.combo = self.insert_combo_list(["Constant", "Reflect", "Replicate"])

        # Insert a signle input box to select the constant value
        self.constant = self.insert_mono_input("Value:", defaultValue=0)
        
        # Insert input boxes to select the padding values
        self.leftRight = self.insert_dual_input("Left-Right:", 0, 0)      
        self.topBottom = self.insert_dual_input("Top-Bottom:", 0, 0)

         # connect widgets to the appropriate combo lists 
        self.set_combo_adapt_widgets(self.combo, [[self.constant, self.leftRight, self.topBottom], 
                                                                [self.leftRight, self.topBottom], [self.leftRight, self.topBottom]])

    def execute(self, imageBGRA, mask):
        # get the padding type based on the selected combo box value
        padCodes = [cv2.BORDER_CONSTANT, cv2.BORDER_REFLECT, cv2.BORDER_REPLICATE]
        selectedId = self.combo.currentIndex()        
        paddingType = padCodes[selectedId]

        # get the input values from the input boxes
        constant = self.get_component_value(self.constant[:1], mins=[0], maxs=[255], defaults=[0])
        lPad, rPad = self.get_component_value(self.leftRight[:2], defaults=[0, 0])
        tPad, bPad = self.get_component_value(self.topBottom[:2], defaults=[0, 0])

        # apply padding
        imageBGRA = processors.apply_padding(imageBGRA, paddingType, lPad, rPad, tPad, bPad, constant)  

        return imageBGRA
