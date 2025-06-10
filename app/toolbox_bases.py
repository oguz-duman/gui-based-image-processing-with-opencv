import uuid
import cv2

from PySide6.QtCore import Qt, Signal, QMimeData
from PySide6.QtGui import QFont, QDrag
from PySide6.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, 
                               QSizePolicy, QFrame, QCheckBox, QComboBox, QFileDialog)

import constants
from gui.gui_components import UiComponents 


def select_image(self):
    """
    Open a file dialog to select an image file and read it using OpenCV.
    Returns:
        image (np.ndarray): The selected image as a NumPy array.
    """
    # Open file dialog to select an image file
    filePath, _ = QFileDialog.getOpenFileName(None, "Select an image file", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp)")

    # Check if a file was selected
    if filePath:
        image = cv2.imread(filePath, cv2.IMREAD_UNCHANGED)      # read the image
        
        if image is None:
            raise ValueError("No input image provided")
        elif len(image.shape) == 2:                             # if image is (h,w)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)
        elif len(image.shape) == 3 and image.shape[2] == 1:     # if image is (h,w,1)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)
        elif len(image.shape) == 3 and image.shape[2] == 3:     # if image is (BGR) (h,w,3)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        elif len(image.shape) == 3 and image.shape[2] == 4:     # if image is (BGRA) (h,w,4)
            pass
        else:
            raise ValueError("Unsupported image format")
        
        return image
    
    


class AddNewBox(QWidget):
    """
    A widget that allows the user to add new toolboxes.
    """
    # Signal to communicate with the main application
    trigger = Signal(str)

    def __init__(self):
        super().__init__()

        self.id = str(uuid.uuid4())                     # generate a unique id for the toolbox

        # make the widget fixed size
        self.setFixedWidth(200)
        
        # set a font size variable
        self.font = QFont()              
        self.font.setPointSize(10)  

        # set the layout for the widget
        mainLayout = QVBoxLayout(self) 
        mainLayout.setContentsMargins(0, 0, 0, 0)

        # create a frame to hold the content
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("QFrame#Frame { border: 2px solid gray; border-radius: 10px; }")
        frame.setObjectName("Frame")
        frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        frame.setFixedWidth(200)
        mainLayout.addWidget(frame)     

        # create a layout inside the frame
        self.frameLayout = QVBoxLayout(frame)
        self.frameLayout.setContentsMargins(10, 10, 10, 10)

        # create a title label
        label = QLabel(constants.ADD_TOOLBOX_TITLE)
        label.setFont(self.font)
        label.setAlignment(Qt.AlignHCenter)
        self.frameLayout.addWidget(label)
        
        # Create a combo box to select the toolbox
        self.combo = QComboBox()
        self.combo.addItems([toolbox['NAME'] for toolbox in constants.TOOLBOXES.values()])
        self.combo.setFont(self.font)
        self.combo.setStyleSheet("padding: 5px;")  
        self.frameLayout.addWidget(self.combo, alignment=Qt.AlignVCenter)
        view = self.combo.view()
        view.setMouseTracking(False)  
        view.setAutoScroll(False)     
    
        # Create a button to add a new method
        newBtn = QPushButton("+")
        font = QFont()              
        font.setPointSize(20)  
        newBtn.setFont(font) 
        newBtn.setStyleSheet("padding-top: 5px; padding-bottom: 10px;")     
        newBtn.clicked.connect(lambda: self.trigger.emit(self.combo.currentText()))  
        self.frameLayout.addWidget(newBtn, alignment=Qt.AlignVCenter)



class Toolbox(QWidget, UiComponents):
    """
    A base class for all toolboxes. It provides a common interface.
    Parameters:
        title (str): The title of the toolbox.
    """
    # Signals to communicate with the main application
    updateTrigger = Signal()
    removeTrigger = Signal(str)
   

    def __init__(self, title="Toolbox"):
        super().__init__()

        self.contentLayout = QVBoxLayout()              # create a layout to hold the content of the toolbox

        self.set_parent(self.contentLayout)             # set the parent layout for the toolbox
        self.set_update_trigger(self.updateTrigger)     # set the update trigger for the toolbox

        self.title = title                      # set the title of the toolbox
        self.id = str(uuid.uuid4())             # generate a unique id for the toolbox
        self.initiate_ui()                      # set up the UI

    def initiate_ui(self):
        """
        Initiate the UI for the toolbox.
        """
        self.setFixedWidth(200)             # make the widget fixed size
        
        # set a font size variable
        self.font = QFont()              
        self.font.setPointSize(10)  

        # set the layout for the widget
        mainLayout = QVBoxLayout(self) 
        mainLayout.setContentsMargins(0, 0, 0, 0)

        # create a frame to hold the content
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("QFrame#Frame { border: 2px solid gray; border-radius: 10px; }")
        frame.setObjectName("Frame")
        frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        frame.setFixedWidth(200)
        mainLayout.addWidget(frame)     

        # create a layout inside the frame
        frameLayout = QVBoxLayout(frame)
        frameLayout.setContentsMargins(10, 10, 10, 10)

        # create a horizontal layout for the title and remove button
        titleLayout = QHBoxLayout()
        frameLayout.addLayout(titleLayout, 1)
        titleLayout.setAlignment(Qt.AlignTop)

        # create a title label
        label = QLabel(self.title)
        label.setFont(self.font)
        titleLayout.addWidget(label)

        # create a button to remove the toolbox
        removeBtn = QPushButton("X")
        removeBtn.setFont(self.font)
        removeBtn.setFixedWidth(30)
        removeBtn.clicked.connect(lambda: self.removeTrigger.emit(self.id))
        titleLayout.addWidget(removeBtn,1)
        
        # create a layout for the ON/OFF switch
        switchLayout = QHBoxLayout()
        frameLayout.addLayout(switchLayout, 1)

        # create ON/OFF switch
        self.switch = QCheckBox("On/Off")
        self.switch.setChecked(True)
        self.switch.setFont(self.font)
        self.switch.stateChanged.connect(lambda: self.updateTrigger.emit())
        self.switch.setFixedHeight(30)
        switchLayout.addWidget(self.switch, alignment=Qt.AlignTop)

        # add the content layout to the frame layout
        frameLayout.addLayout(self.contentLayout, 4)

        # add a dummy widget to fill the space
        dummy = QWidget()
        dummy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.contentLayout.addWidget(dummy)
    

    def update_toolbox(self, imageBGRA):
        """
        Runs only when the toolbox is created for the first time and everytime the input image is changed. 
        """
        self.imageBGRA = imageBGRA



class DraggableToolbox(Toolbox):
    """
    A base class for all toolboxes that can be dragged and dropped.
    """
    def mousePressEvent(self, event):
        """
        Handles the mouse press event to initiate dragging.
        Stores the starting position of the drag when the left mouse button is pressed.
        """
        if event.button() == Qt.LeftButton:
            self.dragStartPosition = event.position()

    def mouseMoveEvent(self, event):
        """
        Handles the mouse move event to perform dragging.
        Initiates a drag operation if the left mouse button is held and the mouse is moved beyond a threshold.
        """
        # Check if the left mouse button is pressed
        if not event.buttons() & Qt.LeftButton:
            return
        # Check if the mouse has moved beyond a small threshold
        if (event.position() - self.dragStartPosition).manhattanLength() < 10:
            return

        drag = QDrag(self)                              # Create a QDrag object to handle the drag operation
        mimeData = QMimeData()                          # Create a QMimeData object to store data for the drag
        drag.setMimeData(mimeData)                      
        drag.setHotSpot(event.position().toPoint())     # Set the hotspot for the drag operation
        drag.setPixmap(self.grab())                     # # Set the pixmap for the drag operation (visual representation)
        drag.exec(Qt.MoveAction)                        # Execute the drag operation with a move action

