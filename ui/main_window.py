from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ui import toolboxes
import constants
from ui.ui_management import UiManagement


class MainWindow(QWidget, UiManagement):
    """
    Main window class for the image processing application.
    This class initializes the UI components and manages drop events for reordering toolboxes.
    """

    def __init__(self):
        super().__init__()  

        # Create main layout and set it to the widget
        self.mainLayout = QVBoxLayout(self) 
        self.mainLayout.setContentsMargins(20, 5, 20, 5) 
        self.mainLayout.setSpacing(15)

        # init top, mid and bottom layouts
        self.init_top_layout()
        self.init_midLayout()
        self.init_bottomLayout()

        # Initialize UI variables in UiManagement
        self.init_ui_variables(self.contentLayout, self.add_new_box, self.in_im_canvas, self.out_im_canvas)  
               

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Recall the pipeline to update the output image when the window is resized
        self.pipeline_on_change()


    def init_top_layout(self):
        """
        Initialize the top layout with two labels for displaying images.
        """
        # Create top layout and add it to the main layout
        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addLayout(topLayout, 55)  

        # Create input image canvas
        self.in_im_canvas = InteractiveCanvas()
        topLayout.addWidget(self.in_im_canvas)

        # create spacer layout to separate the two labels
        spacer = QVBoxLayout()
        topLayout.addLayout(spacer, 1)
  
        # create spacer label
        arrow = QLabel(">")
        font = QFont()              
        font.setPointSize(35)       
        arrow.setFont(font) 
        arrow.setAlignment(Qt.AlignCenter)  
        spacer.addWidget(arrow, 1, alignment=Qt.AlignTop)

        # Create output image canvas
        self.out_im_canvas = InteractiveCanvas()
        topLayout.addWidget(self.out_im_canvas)


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
        btn.clicked.connect(self.open_new_image)   
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 2 - switch to histogram
        btn = QPushButton(constants.HISTOGRAM_BUTTON)
        midLayout.addWidget(btn)   
        btn.clicked.connect(lambda: self.mode_buttons('HISTOGRAM'))   
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 3 - See Layers
        btn = QPushButton(constants.CHANNELS_BUTTON)
        midLayout.addWidget(btn)    
        btn.clicked.connect(lambda: self.mode_buttons('CHANNELS'))   
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 4 - switch to frequency domain
        btn = QPushButton(constants.FREQUENCY_BUTTON)
        midLayout.addWidget(btn)    
        btn.clicked.connect(lambda: self.mode_buttons('FREQUENCY'))   
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 

        # Button 5 - save image
        btn = QPushButton(constants.SAVE_BUTTON)
        midLayout.addWidget(btn)   
        btn.clicked.connect(lambda: self.save_image())   
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
        self.add_new_box.trigger.connect(self.insert_toolbox)  # connect click event to 'add_new_toolbox' method

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
        if source and isinstance(source, toolboxes.Toolbox):
            self.pipeline.move_step(source, index)              # move the function box in the pipeline
            self.contentLayout.removeWidget(source)             # Remove the widget from its current position in the layout
            self.contentLayout.insertWidget(index, source)      # Insert the widget at the new index in the layout

            event.acceptProposedAction()            # Accept the proposed action for the drop event
            self.pipeline_on_change()                     # Rerun the pipeline to update the output image


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



class InteractiveCanvas(FigureCanvas):
    """
    A custom canvas for displaying and interacting with matplotlib figures.
    This canvas supports panning and zooming using mouse events and the scroll wheel.
    """
    def __init__(self, parent=None):
        self.figure = Figure()
        super().__init__(self.figure)
        self.setParent(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self._axes = self.figure.add_subplot(111)
        self._is_panning = False
        self._pan_start = None


    def wheelEvent(self, event):
        """
        Handle the mouse wheel event for zooming in and out of the plot.
        Args:
            event (QWheelEvent): The wheel event containing information about the scroll direction.
        """
        # Check if the axes are set, if not, do nothing
        if self._axes is None:
            return

        # Get the mouse position in data coordinates
        pos = event.position()
        x, y = pos.x(), pos.y()
        xdata, ydata = self._axes.transData.inverted().transform((x, y))

        # Determine the zoom factor based on the scroll direction
        step = event.angleDelta().y()
        factor = 1.2 if step < 0 else 0.8

        # Adjust the x and y limits based on the zoom factor
        xlim = self._axes.get_xlim()
        ylim = self._axes.get_ylim()

        # Calculate new limits based on the zoom factor and the mouse position
        self._axes.set_xlim([
            xdata - (xdata - xlim[0]) * factor,
            xdata + (xlim[1] - xdata) * factor
        ])
        self._axes.set_ylim([
            ydata - (ydata - ylim[0]) * factor,
            ydata + (ylim[1] - ydata) * factor
        ])
        self.draw()     


    def mousePressEvent(self, event):
        """
        Handle the mouse press event to initiate panning.
        Args:
            event (QMouseEvent): The mouse event containing information about the button pressed.
        """
        # Check if the left mouse button is pressed to start panning
        if event.button() == Qt.LeftButton:
            self._is_panning = True
            self._pan_start = event.position()


    def mouseMoveEvent(self, event):
        """
        Handle the mouse move event to update the plot during panning.
        Args:
            event (QMouseEvent): The mouse event containing information about the current position.
        """
        # Check if panning is active and the pan start position is set
        if self._is_panning and self._pan_start:

            # Calculate the distance moved in pixels
            dx = event.position().x() - self._pan_start.x()
            dy = event.position().y() - self._pan_start.y()

            # Convert the pixel movement to data coordinates
            dx_data = dx / self.width() * (self._axes.get_xlim()[1] - self._axes.get_xlim()[0])
            dy_data = dy / self.height() * (self._axes.get_ylim()[1] - self._axes.get_ylim()[0])

            # Update the x and y limits based on the pan distance
            self._axes.set_xlim([
                self._axes.get_xlim()[0] - dx_data,
                self._axes.get_xlim()[1] - dx_data
            ])
            self._axes.set_ylim([
                self._axes.get_ylim()[0] + dy_data,
                self._axes.get_ylim()[1] + dy_data
            ])

            self._pan_start = event.position()
            self.draw()


    def mouseReleaseEvent(self, event):
        """
        Handle the mouse release event to stop panning.
        Args:
            event (QMouseEvent): The mouse event containing information about the button released.
        """
        # Check if the left mouse button is released to stop panning
        if event.button() == Qt.LeftButton:
            self._is_panning = False
            self._pan_start = None

