from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea

from ui import toolboxes
import constants
import utils
from ui.ui_management import UiManagement


class MainWindow(QWidget):
    """
    Main window class for the image processing application.
    This class initializes the UI components and manages drop events for reordering toolboxes.
    """

    def __init__(self):
        super().__init__()  

        # create an instance of the UiManagement class
        self.ui_management = UiManagement()  

        # Create main layout and set it to the widget
        self.mainLayout = QVBoxLayout(self) 
        self.mainLayout.setContentsMargins(20, 5, 20, 5) 
        self.mainLayout.setSpacing(15)

        # init top, mid and bottom layouts
        self.init_top_layout()
        self.init_midLayout()
        self.init_bottomLayout()

        # Initialize UI variables in UiManagement
        self.ui_management.init_ui_variables(self.contentLayout, self.add_new_box, self.leftLabel,
                                              self.rightLabel, self.leftTitle, self.rightTitle,
                                              self.zoomIn, self.zoomOut)  
               

    def init_top_layout(self):
        """
        Initialize the top layout with two labels for displaying images.
        """
        # Create top layout and add it to the main layout
        topLayout = QHBoxLayout()
        self.mainLayout.addLayout(topLayout, 55)  

        # create leftLayout to hold the left image and title
        leftLayout = QVBoxLayout()
        leftLayout.setContentsMargins(0, 0, 0, 0)
        leftLayout.setSpacing(0)
        topLayout.addLayout(leftLayout, 6)

        # create leftTitle label for displaying the input image title
        self.leftTitle = QLabel("")
        leftLayout.addWidget(self.leftTitle, 0.5, alignment=Qt.AlignCenter)

        # Create leftLabel for displaying the input image
        self.leftLabel = QLabel(self)
        pixmap = QPixmap("images/no_image.jpg")
        self.leftLabel.setPixmap(pixmap)
        self.leftLabel.setAlignment(Qt.AlignCenter)
        leftLayout.addWidget(self.leftLabel, 12)

        # create spacer layout to separate the two labels
        spacer = QVBoxLayout()
        topLayout.addLayout(spacer, 1)

        # create zoom layout
        zoomLayout = QHBoxLayout()
        spacer.addLayout(zoomLayout, 1)
        font = QFont()              
        font.setPointSize(12)  

        # create zoom out button
        self.zoomOut = QPushButton("-")
        self.zoomOut.setFixedWidth(40)
        self.zoomOut.setFont(font) 
        self.zoomOut.setStyleSheet("padding-bottom: 2px;")
        self.zoomOut.clicked.connect(lambda: self.ui_management.display_histogram(zoom=-1)) 
        zoomLayout.addWidget(self.zoomOut, 1, alignment=Qt.AlignBottom)
        self.zoomOut.hide()
        
        # create zoom in button
        self.zoomIn = QPushButton("+")
        self.zoomIn.setFixedWidth(40)
        self.zoomIn.setFont(font) 
        self.zoomIn.setStyleSheet("padding-bottom: 2px;")
        self.zoomIn.clicked.connect(lambda: self.ui_management.display_histogram(zoom=1))
        zoomLayout.addWidget(self.zoomIn, 1, alignment=Qt.AlignBottom)
        self.zoomIn.hide()
        
        # create spacer label
        arrow = QLabel(">")
        font = QFont()              
        font.setPointSize(35)       
        arrow.setFont(font) 
        arrow.setAlignment(Qt.AlignCenter)  
        spacer.addWidget(arrow, 1, alignment=Qt.AlignTop)

        # create rightLayout to hold the right image and title
        rightLayout = QVBoxLayout()
        rightLayout.setContentsMargins(0, 0, 0, 0)
        rightLayout.setSpacing(0)
        topLayout.addLayout(rightLayout, 6)

        # create rightTitle label for displaying the output image title
        self.rightTitle = QLabel("")
        rightLayout.addWidget(self.rightTitle, 0.5, alignment=Qt.AlignCenter)

        # Create rightLabel for displaying the output image
        self.rightLabel = QLabel(self)
        pixmap = QPixmap("images/no_image.jpg")
        self.rightLabel.setPixmap(pixmap)
        self.rightLabel.setAlignment(Qt.AlignCenter)
        rightLayout.addWidget(self.rightLabel, 12)


    def init_midLayout(self):
        """
        Initialize the mid layout with buttons for various actions.
        """
        # Create mid layout and add it to the main layout
        midLayout = QHBoxLayout()
        self.mainLayout.addLayout(midLayout, 10) 

        # Create mid layout widgets and add them to the mid layout
        font = QFont()              
        font.setPointSize(10)  
        
        # Button 1 - open image
        btn = QPushButton(constants.OPEN_BUTTON)
        midLayout.addWidget(btn)      
        btn.clicked.connect(self.ui_management.open_new_image)   
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 2 - switch to histogram
        btn = QPushButton(constants.HISTOGRAM_BUTTON)
        midLayout.addWidget(btn)    
        btn.clicked.connect(self.ui_management.switch_to_histogram)   
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 3 - See Layers
        btn = QPushButton(constants.CHANNELS_BUTTON)
        midLayout.addWidget(btn)    
        btn.clicked.connect(self.ui_management.switch_to_colorLayer)  
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 4 - switch to frequency domain
        btn = QPushButton(constants.FREQUENCY_BUTTON)
        midLayout.addWidget(btn)    
        btn.clicked.connect(self.ui_management.switch_to_frequency)  
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 5 - save image
        btn = QPushButton(constants.SAVE_BUTTON)
        midLayout.addWidget(btn)   
        btn.clicked.connect(lambda: utils.save_image(self.ui_management.outputBGRA))   
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 


    def init_bottomLayout(self):
        """
        Initialize the bottom layout with scroll area for function boxes.
        """
        # Create bottom layout and add it to the main layout
        bottomLayout = QHBoxLayout()
        self.mainLayout.addLayout(bottomLayout, 35)
          
        # create scroll area widget and add it to the bottom layout
        scrollArea = QScrollArea()         
        scrollArea.setWidgetResizable(True)        
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
        bottomLayout.addWidget(scrollArea)        
        
        # create content widget and set it to the scroll area
        contentWidget = QWidget()  
        scrollArea.setWidget(contentWidget)  

        # create content layout and set it to the content widget
        self.contentLayout = QHBoxLayout(contentWidget)
        self.contentLayout.setAlignment(Qt.AlignLeft)
                
        # insert 'new function' box
        self.add_new_box = toolboxes.AddNewBox()
        self.contentLayout.addWidget(self.add_new_box)
        self.add_new_box.trigger.connect(self.ui_management.insert_toolbox)  # connect click event to 'add_new_toolbox' method

        # drag and drop functionality
        contentWidget.setAcceptDrops(True)
        contentWidget.dragEnterEvent = self.dragEnterEvent
        contentWidget.dropEvent = self.dropEvent


    def dragEnterEvent(self, event):
        """
        Handle the drag enter event to allow drag-and-drop functionality.
        Args:
            event (QDragEnterEvent): The drag enter event containing information about the dragged data.
        """
        # Check if the event contains mime data and accept the proposed action
        if event.mimeData():
            event.acceptProposedAction()


    def dropEvent(self, event):
        """
        Handle the drop event to allow reordering of function boxes in the pipeline.
        Args:
            event (QDropEvent): The drop event containing information about the dropped data.
        """
        pos = event.position().toPoint()                # Get the position where the item is dropped
        source = event.source()                         # Get the source widget being dragged
        index = self.find_insert_index(pos)             # Find the index where the item should be inserted

        # Check if the source is a valid FunctionBox
        if source and isinstance(source, toolboxes.FunctionBox):
            self.ui_management.pipeline.move_step(source, index)              # move the function box in the pipeline
            self.contentLayout.removeWidget(source)             # Remove the widget from its current position in the layout
            self.contentLayout.insertWidget(index, source)      # Insert the widget at the new index in the layout

            event.acceptProposedAction()            # Accept the proposed action for the drop event
            self.ui_management.pipeline_on_change()                     # Rerun the pipeline to update the output image


    def find_insert_index(self, pos):
        """
        Find the index in the layout where a widget should be inserted based on the drop position.
        Args:
            pos (QPoint): The position where the item is dropped.
        Returns:
            int: The index where the widget should be inserted.
        """
        # Iterate through all widgets in the content layout
        for i in range(self.contentLayout.count()):
            widget = self.contentLayout.itemAt(i).widget()
            # Check if the widget is valid and not the special footer widget (add_new_box)
            if widget and widget != self.add_new_box:
                # If the drop position is within the geometry of the widget, return its index
                if widget.geometry().contains(pos):
                    return i
        # If no suitable position is found, return the last index (before add_new_box)
        return self.contentLayout.count() - 1

