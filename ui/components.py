
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame, QSlider,
                               QCheckBox, QComboBox, QLineEdit, QRadioButton, QButtonGroup, QFileDialog)
from PySide6.QtGui import QFont



class UiComponents():
    """
    """

    def __init__(self, parent, onchance_func):
        
        self.font = QFont()              
        self.font.setPointSize(10) 
        self.parent = parent
        self.on_change = onchance_func

    def mono_input(self, heading, defaultValue=0):
        """
        This function is called to insert a single input box into the function box.
        """

        # layout for the input box
        layout = QHBoxLayout()
        self.parent.addLayout(layout)

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
    

    def dual_input(self, heading, default1=0, default2=255):
        """
        This function is called to insert min and max input boxes into the function box.
        """
        # Input range area
        layout1 = QHBoxLayout()
        self.parent.addLayout(layout1)

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
    

    def triple_input(self, heading, default1=0, default2=0, default3=0):
        """
        """
        # Input range area
        layout1 = QHBoxLayout()
        layout1.setSpacing(0)
        self.parent.addLayout(layout1)

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
    

    def slider(self, heading, minValue, maxValue, defaultValue=0):
        """
        This function is called to insert a slider into the function box.
        """
        # Create a label to display the current value of the slider
        label = QLabel(f"{heading}: {defaultValue}")
        label.setFont(self.font)
        self.parent.addWidget(label, alignment=Qt.AlignLeft)

        # Create a slider to adjust brightness
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(minValue)
        slider.setMaximum(maxValue)
        slider.setValue(defaultValue)
        slider.valueChanged.connect(self.on_change)
        self.parent.addWidget(slider)

        return [slider, label]


    def radio_buttons(self, headings=[]):
        """
        This function is called to insert radio buttons into the function box.
        It creates a vertical layout for the radio buttons and adds them to the content layout.
        """
        # layout for radio buttons
        layout = QVBoxLayout()
        self.parent.addLayout(layout)

        # create a button group to hold the radio buttons
        buttonGroup = QButtonGroup(self)  
        buttonGroup.buttonClicked.connect(self.on_change)      

        # create radio buttons
        for i, heading in enumerate(headings):
            radio = QRadioButton(heading)
            buttonGroup.addButton(radio, i)            
            radio.setFont(self.font)
            layout.addWidget(radio, alignment=Qt.AlignLeft)
        
        # click the first button by default
        if buttonGroup.buttons():
            buttonGroup.buttons()[0].setChecked(True)

        return buttonGroup


    def combo_list(self, headings=[]):
        """
        This function is called to insert a combo box into the function box.
        """
        combo = QComboBox()
        combo.addItems(headings)
        combo.setFont(self.font)
        combo.currentIndexChanged.connect(self.on_change)       # onchange event for the combo box
        self.parent.addWidget(combo)                     # add the combo box to the content layout

        return combo


    def switch(self, heading):
        """
        This function is called to insert a switch into the function box.
        """
        onOff = QCheckBox(heading)
        onOff.setChecked(False)
        onOff.setFont(self.font)
        onOff.stateChanged.connect(self.on_change)
        onOff.setFixedHeight(30)
        self.parent.addWidget(onOff)

        return onOff


    def button(self, heading):
        """
        This function is called to insert a button into the function box.
        """
        button = QPushButton(heading)
        button.setFont(self.font)
        button.setFixedHeight(30)
        self.parent.addWidget(button)

        return button

