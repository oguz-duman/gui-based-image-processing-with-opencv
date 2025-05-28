# GUI-Based Image Processing with OpenCV

This project is a PySide6-based graphical user interface (GUI) application built on OpenCV that provides an interactive platform for image processing. It currently includes common techniques such as histogram equalization, filtering, and thresholding, but is designed with a modular architecture to allow easy addition of new image processing methods. Users can apply various operations on input images and observe the results in real time, making it both a practical tool and a flexible framework for experimentation and extension.



![Screenshot](images/app.png)



## How to Install

1. Make sure you have Python 3.7+ installed.  
2. Clone this repository:  
git clone https://github.com/ouzdu-s/gui-based-image-processing-with-opencv.git

3. Navigate to the project directory:  
cd gui-based-image-processing-with-opencv
4. Install required packages:  
pip install -r requirements.txt


## How to Use

1. Run the main Python script `main.py` to launch the GUI:
2. Use the GUI buttons to load an image.  
3. Select desired image processing methods from the menu.  
4. Observe the processed image in real-time.  
5. Export the resulting images as needed.


## Code Structure

* The application is organized around six main classes, each with a specific role:

* `MainWindow`: Initializes the GUI and manages the main layout of the application.

* `UIManagement`: Handles user interactions such as drag-and-drop, switching between multiple views (e.g., histogram or color layers), file selection etc.

* `Pipeline`: Manages operations like adding, removing, reordering, and executing toolboxes in the order they are applied.

* `Toolboxes`: Each image processing method is represented as an independent toolbox (e.g., BrightnessBox, ContrastBox). These toolboxes are the core interactive modules that users can add to the processing pipeline.

* To avoid repetitive code and speed up toolbox development, all toolboxes inherit from two base classes:

* `UIComponents`: Provides reusable GUI elements like buttons, sliders, and input fields.

* `Processor`: Contains the actual image processing functions, built using OpenCV.


## How to Add Your Own Image Processing Methods

This project is designed to be modular and easily extensible. To add a new image processing method, follow these steps:

1. add the display name of the new method and its corresponding class name to the `TOOLBOXES` list in the `constants.py` file.
2. create a new class in the `toolboxes.py` file that inherits from `DraggableToolbox`. Use the class name you defined in the `TOOLBOXES` list.
3. implement the `__init__` method to set up the GUI elements for your toolbox. You can directly insert pre_created components from `components.py`.
4. implement the `execute` method to define the image processing steps for your toolbox. It should return the processed image in the BGRA format. You can directly use the pre_created image processing methods from `processor.py` or implement your own logic.
