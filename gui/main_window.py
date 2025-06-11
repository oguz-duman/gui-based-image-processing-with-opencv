import cv2

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from app import toolbox_bases
import constants
import colors
from gui.gui_management import GUiManagement
from gui.gui_components import NoArrowComboBox


class MainWindow(QWidget, GUiManagement):
    """
    Main window class for the image processing application.
    This class initializes the UI components and manages drop events for reordering toolboxes.
    """

    def __init__(self):
        super().__init__()  

        # Create main layout and set it to the widget
        self.main_layout = QVBoxLayout(self) 
        self.main_layout.setContentsMargins(20, 5, 20, 5) 
        self.main_layout.setSpacing(15)

        # init top, mid and bottom layouts
        self.init_top_layout()
        self.init_midLayout()
        self.init_bottomLayout()

        # Initialize UI variables in UiManagement
        self.init_ui_variables(self.contentLayout, self.add_new_box, self.in_im_canvas, self.out_im_canvas, self.left_title, self.right_title)  

        # read and display a placeholder image
        initial_im = cv2.imread('images/no_image.png', cv2.IMREAD_UNCHANGED)  
        self.display_images([initial_im, initial_im])


    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Recall the pipeline to update the output image when the window is resized
        self.pipeline_on_change()
        

    def init_top_layout(self):
        """
        Initialize the top layout with two labels for displaying images.
        """
        # Create top layout and add it to the main layout
        top_layout = QHBoxLayout()
        self.main_layout.addLayout(top_layout, 55)  

        # create leftLayout to hold the left image and title
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        top_layout.addLayout(left_layout, 48)

        # create leftTitle label for displaying the input image title
        self.left_title = QLabel("")
        self.left_title.setText("Channel")
        left_layout.addWidget(self.left_title, alignment=Qt.AlignCenter)
        self.left_title.hide()

        # Create input image canvas
        self.in_im_canvas = InteractiveCanvas()  
        left_layout.addWidget(self.in_im_canvas)

        # create spacer layout to separate the two labels
        spacer = QVBoxLayout()
        top_layout.addLayout(spacer, 4)
  
        # create spacer label
        arrow = QLabel(">")
        font = QFont()              
        font.setPointSize(35)       
        arrow.setFont(font) 
        arrow.setAlignment(Qt.AlignCenter)  
        spacer.addWidget(arrow, 1, alignment=Qt.AlignCenter)

        # create rightLayout to hold the right image and title
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        top_layout.addLayout(right_layout, 48)

        # create rightTitle label for displaying the output image title
        self.right_title = QLabel("")
        right_layout.addWidget(self.right_title, alignment=Qt.AlignCenter)
        self.right_title.hide()

        # Create output image canvas
        self.out_im_canvas = InteractiveCanvas()
        right_layout.addWidget(self.out_im_canvas)


    def init_midLayout(self):
        """
        Initialize the mid layout with buttons for various actions.
        """
        # Create mid layout and add it to the main layout
        midLayout = QHBoxLayout()
        self.main_layout.addLayout(midLayout, 10) 

        # Create mid layout widgets and add them to the mid layout
        font = QFont()              
        font.setPointSize(10)  
        
        # Button 1 - open image
        btn = QPushButton(constants.OPEN_BUTTON)
        midLayout.addWidget(btn, 1)      
        btn.clicked.connect(self.open_new_image)   
        btn.setFlat(True)
        btn.setFont(font) 
        btn.setStyleSheet(f"""
            QPushButton {{
                padding-top: 10px;
                padding-bottom: 10px;
            }}
            QPushButton:hover {{
                background-color: {colors.COMBO_HOVER};
            }}
        """)

        # List 1 - Visualization type
        visualization_type = NoArrowComboBox(items=constants.VISUALIZATION_TYPES)
        midLayout.addWidget(visualization_type, 1)
        visualization_type.setFont(font)
        visualization_type.currentTextChanged.connect(lambda: self.switch_view(visualization_type.currentText()))  

        # List 2 - Color Channel
        color_chan = NoArrowComboBox(items=constants.COLOR_CHANNELS)
        midLayout.addWidget(color_chan, 1)
        color_chan.setFont(font)
        color_chan.currentTextChanged.connect(lambda: self.switch_color_chan(color_chan.currentText())) 

        # Button 2 - save image
        btn = QPushButton(constants.SAVE_BUTTON)
        midLayout.addWidget(btn, 1)   
        btn.clicked.connect(lambda: self.save_image())   
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 
        btn.setStyleSheet(f"""
            QPushButton {{
                padding-top: 10px;
                padding-bottom: 10px;
            }}
            QPushButton:hover {{
                background-color: {colors.COMBO_HOVER};
            }}
        """)


    def init_bottomLayout(self):
        """
        Initialize the bottom layout with scroll area for function boxes.
        """
        # Create bottom layout and add it to the main layout
        bottomLayout = QHBoxLayout()
        self.main_layout.addLayout(bottomLayout, 35)
          
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
        self.add_new_box = toolbox_bases.AddNewBox()
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
        if source and isinstance(source, toolbox_bases.Toolbox):
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
        self.figure = Figure(facecolor=(1,1,1,0))

        super().__init__(self.figure)
        self.setParent(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self._axes = self.figure.add_subplot(111)               # Create a single axes 
        self.configuration_types()                              # Set the initial configuration for the canvas

        # Initialize panning variables 
        self._is_panning = False
        self._pan_start = None

        # Variables to store x a nd y limits for zooming and panning
        self._xlim = None
        self._ylim = None

        # Variables to store original x and y limits for zooming and panning limits
        self._orig_xlim = None
        self._orig_ylim = None

        # Set the canvas to be transparent
        self.setStyleSheet("background: transparent;")  


    def wheelEvent(self, event):
        """
        Handle the mouse wheel event for zooming in and out of the plot.
        Args:
            event (QWheelEvent): The wheel event containing information about the scroll direction.
        """
        if self._axes is None:
            return

        pos = event.position()
        x, y = pos.x(), pos.y()
        xdata, ydata = self._axes.transData.inverted().transform((x, y))

        xlim = self._axes.get_xlim()
        ylim = self._axes.get_ylim()

        step = event.angleDelta().y()
        factor = 1.05 if step < 0 else 0.95

        # calculate new limits
        self._xlim = [
            xdata - (xdata - xlim[0]) * factor,
            xdata + (xlim[1] - xdata) * factor
        ]
        self._ylim = [
            ydata - (ydata - ylim[0]) * factor,
            ydata + (ylim[1] - ydata) * factor
        ]

        # ensure the new limits do not go below 0 or exceed original limits
        self._xlim[0] = max(0, self._xlim[0])  
        self._ylim[1] = max(0, self._ylim[1])  
        self._xlim[1] = min(self._orig_xlim[1], self._xlim[1]) 
        self._ylim[0] = min(self._orig_ylim[0], self._ylim[0])  

        # Update the axes limits and redraw the canvas
        self._axes.set_xlim(self._xlim)
        self._axes.set_ylim(self._ylim)
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
            self._xlim = [
                self._axes.get_xlim()[0] - dx_data,
                self._axes.get_xlim()[1] - dx_data
            ]
            self._ylim = [
                self._axes.get_ylim()[0] + dy_data,
                self._axes.get_ylim()[1] + dy_data
            ]

            # ensure the new limits do not go below 0 or exceed original limits
            if not (self._xlim[0] < 0 or self._xlim[1] > self._orig_xlim[1]):
                self._axes.set_xlim(self._xlim)
            
            if not (self._ylim[1] < 0 or self._ylim[0] > self._orig_ylim[0]):
                self._axes.set_ylim(self._ylim)

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


    def configuration_types(self, type="image"):
        """
        Configure the canvas based on the type of content to be displayed.
        Args:
            type (str): The type of content to be displayed. Can be "image" or "histogram".
        """
        if type == "image":
            self._axes.axis('off')  
            self._axes.grid(False)
            self.figure.set_facecolor((1,1,1,0))  
            self.figure.subplots_adjust(left=0, right=1, top=1, bottom=0)       # Adjust the subplot to fill the canvas

        elif type == "histogram":
            self._axes.axis('on')  
            self._axes.grid(True)
            self.figure.set_facecolor((1,1,1,1)) 
            self.figure.tight_layout(pad=1.5)
            self._axes.set_aspect('auto')  
