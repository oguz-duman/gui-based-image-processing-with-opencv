from app.toolbox_bases import DraggableToolbox
import constants
from app import processors

class OrderStatBox(DraggableToolbox):
    """
    A class to create an order statistics toolbox.
    Applies order statistics filtering to the input image.
    Available methods are Median, Max, and Min.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['ORDER_STAT']['NAME'])

        # insert nedded input widgets
        self.combo = self.insert_combo_list(["Median", "Max", "Min"])
        self.kernel = self.insert_mono_input("Kernel Size:", defaultValue=3)

         # connect widgets to the appropriate combo lists 
        self.set_combo_adapt_widgets(self.combo, [[self.kernel], [self.kernel], [self.kernel]])

    def execute(self, imageBGRA, mask):
        # get the kernel size and make sure it is odd
        w = self.get_component_value(self.kernel[:1], mins=[0], defaults=[3])         
        w = w if w % 2 == 1 else w + 1                                      
        
        # apply the selected smoothing method
        if self.combo.currentText() == "Median":
            imageBGRA = processors.apply_order_stat_filter(imageBGRA, w, "median", mask)  
        elif self.combo.currentText() == "Max":
            imageBGRA = processors.apply_order_stat_filter(imageBGRA, w, "max", mask)  
        elif self.combo.currentText() == "Min":
            imageBGRA = processors.apply_order_stat_filter(imageBGRA, w, "min", mask)   

        return imageBGRA
