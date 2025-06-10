from app.toolbox_bases import DraggableToolbox
import constants
from app import processors


class FrequencyFilterBox(DraggableToolbox):
    """
    A class to create a frequency domain filtering toolbox.
    Applies low-pass or high-pass filtering to the input image in the frequency domain.
    """
    def __init__(self):
        super().__init__(constants.TOOLBOXES['FREQ_FILTER']['NAME'])

        # insert a combo list to select the filter type
        self.combo = self.insert_combo_list(["Low Pass", "High Pass"])
        
        # insert a slider to select the filter radius
        self.filter_radius = self.insert_slider(heading="Filter Radius:", minValue=1, maxValue=200, defaultValue=30)
        

    def execute(self, imageBGRA, mask):

        filter_radius = self.filter_radius[0].value()          # get the first filter radius value
        filter_type = self.combo.currentText()                   # get the selected filter type from combo box
        
        # apply the selected frequency filter
        imageBGRA = processors.apply_frequency_filter(imageBGRA, filter_radius, filter_type)

        return imageBGRA