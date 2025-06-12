from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import (QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSlider,
                               QCheckBox, QComboBox, QLineEdit, QRadioButton, QButtonGroup, QStyledItemDelegate)
from PySide6.QtGui import QFont

import colors
      

class GUiComponents():
    """
    This class contains the UI components for the application.
    It provides methods to create and manage various UI elements such as input boxes, sliders, radio buttons, etc.
    It also handles the events triggered by these components.
    Args:
        parent_widget (QWidget): The parent widget to which the UI components will be added.
        onchange_trigger (Signal): The signal to be emitted when the value of any input box is changed.
    """
    def __init__(self):
        # create a base font for the UI components
        self.font = QFont()              
        self.font.setPointSize(10) 

        self.trigger = None          # signal to be emitted when the value of any input box is changed


    def set_parent(self, parent_widget):
        """
        This method sets the parent widget for the UI components.
        Args:
            parent_widget (QWidget): The parent widget to which the UI components will be added.
        """
        self.parent_widget = parent_widget


    def set_update_trigger(self, trigger):
        """
        This method sets the signal to be emitted when the value of any input box is changed.
        Args:
            onchange_trigger (Signal): The signal to be emitted when the value of any input box is changed.
        """
        self.trigger = trigger


    def on_change(self, new_value=None, label=None):
        """
        This method is called when the value of any input box is changed.
        It updates the label text to reflect the new value and emits the trigger signal.
        Args:
            new_value (str): The new value of the input box.
            label (QLabel): The label associated with the input box.
        """
        # if a new value is provided, update the label text 
        if label is not None:
            label.setText(f"{label.text().split(':')[0]}: {new_value}")

        # If a trigger signal is set, emit the signal to notify that the value has changed
        if self.trigger is not None:
            self.trigger.emit()                     


    def combo_on_change(self, new_index, adapt_widgets=[]):
        """
        This method is called when the index of the combo box is changed.
        It shows or hides the widgets associated with the selected index.
        Args:
            new_index (int): The index of the selected item in the combo box.
            adapt_widgets (list): A list of lists containing the widgets to be shown or hidden.
        """
        # Hide all widgets in the adapt_widgets list
        if adapt_widgets:
            for i, group in enumerate(adapt_widgets):
                for widgets in group:
                    for widget in widgets:
                        widget.hide()
                        
        # Show the widgets corresponding to the selected index
        if adapt_widgets:
            for i, group in enumerate(adapt_widgets):
                if i == new_index:
                    for widgets in group:
                        for widget in widgets:
                            widget.show()
                    break


    def get_component_value(self, widgets, mins=None, maxs=None, defaults=None):
        """
        This method retrieves the values from the input boxes and validates them.
        It returns the values as a list of integers or floats.
        Args:
            widgets (list): A list of input boxes to retrieve values from.
            mins (list): A list of minimum values for each input box to validate against.
            maxs (list): A list of maximum values for each input box to validate against.
            defaults (list): A list of default values for each input box if the input is invalid.
        """
        # set default values for mins, maxs, and defaults if not provided
        mins = [0] * len(widgets) if mins is None else mins
        maxs = [float('inf')] * len(widgets) if maxs is None else maxs
        defaults = [0] * len(widgets) if defaults is None else defaults
        
        try:
            values = []
            # iterate through the widgets and get their values
            for widget, min, max, default in zip(widgets, mins, maxs, defaults):
                values.append(int(widget.text()) if min <= int(widget.text()) <= max else default)
            
            return values[0] if len(values) == 1 else values        # return a list or a single value based on the number of inputs
        except:
            return defaults[0] if len(defaults) == 1 else defaults  # return a list or a single value based on the number of inputs
    

    def insert_mono_input(self, heading, defaultValue=0, parent=None):
        """
        This method creates a single input box for the user to enter a value.
        Args:
            heading (str): The label for the input box.
            defaultValue (int): The default value to be displayed in the input box.
        Returns:
            list: A list containing the input box and its label.
        """
        # if a parent widget is provided, use it; otherwise, use the main parent widget
        parent = self.parent_widget if parent is None else parent

        # layout for the input box
        layout = QHBoxLayout()
        parent.addLayout(layout)

        # heading for the input
        label = QLabel(heading)
        label.setFont(self.font)
        layout.addWidget(label, alignment=Qt.AlignLeft)

        # input box for the value 
        inArea = QLineEdit()
        inArea.setFont(self.font)
        inArea.setText(str(defaultValue))
        inArea.setFixedWidth(40)
        inArea.textChanged.connect(self.on_change)
        layout.addWidget(inArea, alignment=Qt.AlignLeft)

        return [inArea, label]
    

    def insert_dual_input(self, heading, default1=0, default2=255, parent=None):
        """
        This method creates two input boxes for the user to enter a range of values.
        Args:
            heading (str): The label for the input boxes.
            default1 (int): The default minimum value to be displayed in the first input box.
            default2 (int): The default maximum value to be displayed in the second input box.
        Returns:
            list: A list containing the two input boxes and their label.
        """
        # if a parent widget is provided, use it; otherwise, use the main parent widget
        parent = self.parent_widget if parent is None else parent

        # Input range area
        layout1 = QHBoxLayout()
        parent.addLayout(layout1)

        # an indicator for input range
        inLabel = QLabel(heading)
        inLabel.setFont(self.font)
        layout1.addWidget(inLabel)

        # min value for input range 
        inRangeMin = QLineEdit()
        inRangeMin.setFont(self.font)
        inRangeMin.setText(str(default1))
        inRangeMin.setFixedWidth(40)
        inRangeMin.textChanged.connect(self.on_change)
        layout1.addWidget(inRangeMin)

        # max value for input range
        inRangeMax = QLineEdit()
        inRangeMax.setFont(self.font)
        inRangeMax.setText(str(default2))
        inRangeMax.setFixedWidth(40)
        inRangeMax.textChanged.connect(self.on_change)
        layout1.addWidget(inRangeMax)

        return [inRangeMin, inRangeMax, inLabel]
    

    def insert_triple_input(self, heading, default1=0, default2=0, default3=0, parent=None):
        """
        This method creates three input boxes for the user to enter a range of values.
        Args:
            heading (str): The label for the input boxes.
            default1 (int): The default minimum value to be displayed in the first input box.
            default2 (int): The default maximum value to be displayed in the second input box.
            default3 (int): The default maximum value to be displayed in the third input box.
        Returns:
            list: A list containing the three input boxes and their label.
        """
        # if a parent widget is provided, use it; otherwise, use the main parent widget
        parent = self.parent_widget if parent is None else parent

        # Input range area
        layout1 = QHBoxLayout()
        layout1.setSpacing(0)
        parent.addLayout(layout1)

        # an indicator for input range
        label = QLabel(heading)
        label.setFont(self.font)
        layout1.addWidget(label)

        # min value for input range 
        value1 = QLineEdit()
        value1.setFont(self.font)
        value1.setText(str(default1))
        value1.setFixedWidth(40)
        value1.textChanged.connect(self.on_change)
        layout1.addWidget(value1)

        # max value for input range
        value2 = QLineEdit()
        value2.setFont(self.font)
        value2.setText(str(default2))
        value2.setFixedWidth(40)
        value2.textChanged.connect(self.on_change)
        layout1.addWidget(value2)

        # max value for input range
        value3 = QLineEdit()
        value3.setFont(self.font)
        value3.setText(str(default3))
        value3.setFixedWidth(40)
        value3.textChanged.connect(self.on_change)
        layout1.addWidget(value3)

        return [value1, value2, value3, label]
    

    def insert_slider(self, heading, minValue, maxValue, defaultValue=0, rescale=1, parent=None):
        """
        This method creates a slider for the user to adjust a value.
        Args:
            heading (str): The label for the slider.
            minValue (int): The minimum value of the slider.
            maxValue (int): The maximum value of the slider.
            defaultValue (int): The default value to be displayed on the slider.
            rescale (int): A factor to rescale the slider value.
        Returns:
            list: A list containing the slider and its label.
        """
        # if a parent widget is provided, use it; otherwise, use the main parent widget
        parent = self.parent_widget if parent is None else parent

        # Create a label to display the current value of the slider
        label = QLabel(f"{heading}: {defaultValue}")
        label.setFont(self.font)
        parent.addWidget(label, alignment=Qt.AlignLeft)

        # Create a slider to adjust brightness
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(minValue)
        slider.setMaximum(maxValue)
        slider.setValue(defaultValue)
        
        # connect the slider value changed event to the on_change method
        slider.valueChanged[int].connect(lambda new_value: self.on_change(new_value if rescale == 1 else new_value/rescale, label))
        # call the on_change method to set the initial value of the label
        self.on_change(slider.value() if rescale == 1 else slider.value()/rescale, label)  
        
        parent.addWidget(slider)

        return [slider, label]


    def insert_radio_buttons(self, headings=[], parent=None):
        """
        This method creates a group of radio buttons for the user to select an option.
        Args:
            headings (list): A list of labels for the radio buttons.
        Returns:
            list: A list containing the radio buttons and their label.
        """
        # if a parent widget is provided, use it; otherwise, use the main parent widget
        parent = self.parent_widget if parent is None else parent

        # layout for radio buttons
        layout = QVBoxLayout()
        parent.addLayout(layout)

        # create a button group to hold the radio buttons
        radio_buttons = QButtonGroup(None)  
        radio_buttons.buttonClicked.connect(self.on_change)      

        # create radio buttons
        for i, heading in enumerate(headings):
            radio = QRadioButton(heading)
            radio_buttons.addButton(radio, i)            
            radio.setFont(self.font)
            layout.addWidget(radio, alignment=Qt.AlignLeft)
        
        # click the first button by default
        if radio_buttons.buttons():
            radio_buttons.buttons()[0].setChecked(True)

        return [radio_buttons]


    def insert_combo_list(self, headings=[], parent=None):
        """
        This method creates a combo box for the user to select an option from a list.
        Args:
            headings (list): A list of labels for the combo box items.
        Returns:
            QComboBox: The combo box containing the list of items.
        """
        # if a parent widget is provided, use it; otherwise, use the main parent widget
        parent = self.parent_widget if parent is None else parent

        combo = ArrowComboBox(headings)
        combo.setFont(self.font)
        combo.currentIndexChanged.connect(self.on_change)       # onchange event to emit the signal indicating the value has changed
        parent.addWidget(combo)                                 # add the combo box to the content layout

        return combo
    

    def set_combo_adapt_widgets(self, combo, adapt_widgets):
        """
        This method sets up the combo box to show or hide widgets based on the selected index.
        Args:
            combo (QComboBox): The combo box to be set up.
            adapt_widgets (list): A list of lists containing the widgets to be shown or hidden based on the selected index.
        """
        # onchange event to show/hide widgets based on the selected index
        combo.currentIndexChanged[int].connect(lambda new_index: self.combo_on_change(new_index, adapt_widgets))    
        
        # call the function to set the initial state of the widgets   
        self.combo_on_change(combo.currentIndex(), adapt_widgets)  


    def insert_switch(self, heading, setChecked=False, parent=None):
        """
        This method creates a switch (checkbox) for the user to toggle an option.
        Args:
            heading (str): The label for the switch.
        Returns:
            list: A list containing the switch and its label.
        """
        # if no parent is provided, use the main parent widget
        parent = self.parent_widget if parent is None else parent

        switch = QCheckBox(heading)
        switch.setChecked(setChecked)
        switch.setFont(self.font)
        switch.stateChanged.connect(self.on_change)
        switch.setFixedHeight(30)
        parent.addWidget(switch)

        return [switch]


    def insert_button(self, heading, parent=None):
        """
        This method creates a button for the user to click.
        Args:
            heading (str): The label for the button.
        Returns:
            list: A list containing the button.
        """
        # if no parent is provided, use the main parent widget
        parent = self.parent_widget if parent is None else parent

        button = QPushButton(heading)
        button.setFont(self.font)
        button.setFixedHeight(30)
        parent.addWidget(button)

        return [button]
    


class CenteredDelegate(QStyledItemDelegate):
    """
    This class extends QStyledItemDelegate to center the text in the items of a combo box.
    """
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter



class NoArrowComboBox(QComboBox):
    """
    This class extends QComboBox to create a combo box that does not show the arrow button and adapts to light/dark themes.
    Args:
        items (list): A list of items to be added to the combo box.
    """
    def __init__(self, items):
        super().__init__()
        self.popup_open = False

        self.addItems(items)
        self.setEditable(True)
        self.lineEdit().setAlignment(Qt.AlignCenter)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().installEventFilter(self)

        view = self.view()
        view.setMouseTracking(True)  
        view.setAutoScroll(False) 
        view.setStyleSheet(f"""
            QAbstractItemView {{
                show-decoration-selected: 1; 
                outline: 0;
            }}
            QAbstractItemView::item {{
                padding: 2px;
                border-left: 1px solid transparent; 
            }}
            QAbstractItemView::item:selected {{
                background-color: {colors.COMBO_ITEM_HOVER};  
                border-left: 1px solid {colors.COMBO_SELECTED}; 
            }}
        """)

        self.setItemDelegate(CenteredDelegate(self))
        self.setStyleSheet(F"""
            QComboBox {{
                background-color: {colors.COMBO_BACKGROUND};
                padding-top: 8px;
                padding-bottom: 8px;
            }}
            QComboBox:hover {{
                background-color: {colors.COMBO_HOVER};
            }}                                         
        """)

        self.currentIndexChanged.connect(self.line_edit_style)


    def eventFilter(self, obj, event):
        if obj == self.lineEdit() and event.type() in [QEvent.MouseButtonPress, QEvent.MouseButtonDblClick]:
            if self.popup_open:
                self.hidePopup()
                self.popup_open = False
            else:
                self.showPopup()
                self.popup_open = True
            return True
        
        elif event.type() in [QEvent.MouseMove, QEvent.ContextMenu, QEvent.MouseButtonRelease]:
            return True     # ignore these events to prevent unwanted behavior  
                
        return super().eventFilter(obj, event)
        

    def paintEvent(self, event):
        from PySide6.QtWidgets import QComboBox, QStyleOptionComboBox, QStyle, QApplication
        from PySide6.QtWidgets import QStylePainter

        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)

        opt.subControls = QStyle.SC_ComboBoxFrame | QStyle.SC_ComboBoxEditField

        opt.rect.setRight(opt.rect.right())  

        painter = QStylePainter(self)
        painter.drawComplexControl(QStyle.CC_ComboBox, opt)
        painter.drawControl(QStyle.CE_ComboBoxLabel, opt)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        if self.lineEdit():
            self.line_edit_style()


    def line_edit_style(self):
        self.lineEdit().resize(self.width(), self.height())
        self.lineEdit().move(0, 0)
        self.lineEdit().setStyleSheet("background-color: #3c3d3d;")




class ArrowComboBox(QComboBox):
    """
    This class extends QComboBox to create a combo box that adapts to light/dark themes.
    Args:
        items (list): A list of items to be added to the combo box.
    """
    def __init__(self, items):
        super().__init__()

        self.addItems(items)
        
        view = self.view()
        view.setMouseTracking(True)  
        view.setAutoScroll(False) 
        view.setStyleSheet(F"""
            QAbstractItemView {{
                show-decoration-selected: 1; 
                outline: 0;
            }}
            QAbstractItemView::item {{
                padding: 2px;
                border-left: 1px solid transparent; 
            }}
            QAbstractItemView::item:selected {{
                background-color: {colors.COMBO_ITEM_HOVER};  
                border-left: 1px solid {colors.COMBO_SELECTED}; 
            }}
        """)

        self.setStyleSheet(F"""
            QComboBox {{
                padding: 5px;
                padding: 5px; 
                padding-left: 10px; 
                background-color: {colors.COMBO_BACKGROUND};
            }}
        """)

         
      