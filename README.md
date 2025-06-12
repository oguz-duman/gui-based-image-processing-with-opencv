# impros

This project is a PySide6-based graphical user interface (GUI) application that provides an interactive platform for image processing. It supports the implementation of custom methods, from basic operations to advanced image processing algorithms. Users can apply various transformations to input images and observe the results in real time. The application can serve both as a ready-to-use tool and as a flexible framework for custom development and experimentation.

![Screenshot](images/app.png)

---
## How to Install

### Option 1: Download the Executable
1. Go to the Releases page.
2. Download the appropriate release for your operating system.
3. Run the executable — no installation or setup required.

### Option 2: Run from Source

1. Make sure you have Python 3.7+ installed.  
2. Clone this repository:  
```
git clone https://github.com/ouzdu-s/gui-based-image-processing-with-opencv.git
```
3. Navigate to the project directory:  
```
cd gui-based-image-processing-with-opencv
```
4. Install required packages:  
```
pip install -r requirements.txt
```
5. Run the main Python script `main.py` to launch the GUI:  
```
python main.py
```

---
## How to Use

1. Launch the application. 
2. Use the GUI buttons to load an image.  
3. Select desired image processing methods from the bottom menu.  
4. Observe the processed image in real-time.  
5. Export the resulting images as needed.

---
## Code Structure
The application is organized into two main layers: `gui` and `app`.
- #### `gui/` – User Interface Layer
    - This layer defines the GUI logic and visual structure of the application:
    - `main_window.py`: Initializes the main window and overall layout.
    - `gui_management.py`: Handles GUI interactions such as drag-and-drop and view toggling.
    - `gui_components.py`: Contains reusable widgets (buttons, sliders, inputs) used throughout the interface.
- #### `app/` – Application Logic Layer
    - This layer encapsulates the core logic and image processing behavior.
    - `pipeline.py`: Manages the sequence of processing steps.
    - `toolbox_bases.py`: Defines base classes for toolboxes, unifying their behavior and appearance.
    - `processor_utils.py`: Includes helper functions shared across multiple processors.
    - `toolboxes/`: Contains GUI modules (e.g., `BrightnessBox`, `ContrastBox`) representing individual image operations.
    - `processors/`: Contains the algorithmic implementations (e.g., `brightness.py`, `contrast.py`), each tied to toolboxes.

---
## How to Add Your Own Image Processing Methods
This project is designed to be modular and easy to extend. To add a new image processing tool, follow these steps:

1. **Register the Toolbox**  
    Update the `TOOLBOXES` list in `constants.py` by adding a new dictionary entry. Use the following structure:

    ```python
    "YOUR_METHOD": { 
        "NAME": "Your Method Name", 
        "CLASS": "YourMethodBox" 
    }
    ```

2. **Create the Toolbox**  
    Create a new module `YourMethodBox.py` inside the `app/toolboxes/` directory.
    Define a class with the same name you used in the CLASS field above. This class must inherit from DraggableToolbox. Use the following structure:
   
    ```python
    from app.toolbox_bases import DraggableToolbox
    from app import processors
    import constants

    class YourMethodBox(DraggableToolbox):
        def __init__(self):
            super().__init__(constants.TOOLBOXES['YOUR_METHOD']['NAME'])

            # Insert your UI components here, for example:
            self.brightness_slider = self.insert_slider(heading="Brightness", minValue=-100, maxValue=100)

        def execute(self, imageBGRA, mask):
            # Apply your image processing logic here, For example:
            imageBGRA = processors.adjust_brightness(imageBGRA, self.brightness_slider[0].value(), mask=mask)

            return imageBGRA
    ```

    Don't forget to import your toolbox in `app/toolboxes/__init__.py`:
    
    ```python
    from .YourMethodBox import YourMethodBox
    ```

4. **Add GUI Components:**  
    You have two options for adding GUI elements:
    - Use predefined GUI components like slider, buttons etc.  
    These are defined in `gui/gui_components.py`. Simply call them in your toolbox. For example:

       ```python
        self.brightness_slider = self.insert_slider(heading="Brightness", minValue=-100, maxValue=100)
        ```
    - Create Custom GUI components.  
        Define new components as methods inside the UiComponents class in `gui/gui_components.py`. Here's a template:

        ```python
        def your_gui_component(self, parent=None):

            # Keep this line unchanged to ensure the component is added to the correct parent widget.
            parent = self.parent_widget if parent is None else parent

            # Create your GUI component here, for example:
            component = QCheckBox("heading")

            # Make sure you have the following two lines for component to work correctly:
            component.stateChanged.connect(self.on_change)
            parent.addWidget(component)

            return component
        ```
        Then you can simply call the created GUI component in your toolbox:
        ```python
        self.your_component = self.your_gui_component()
        ```

6. **Add Image Processing Logic**  
    You have two options for adding Image Processing Logic:  
    - Use predefined methods from `app/processors/` directory:  

      ```python
        from app import processors
        image = processors.some_method(image)
        ```
    - Create Custom Methods  
        Create a new module `your_method.py` inside the `app/processors/` directory. Here's a basic structure:  

      ```python
      import cv2
      
      def your_method(imageBGRA):
          # implement your image processing logic here, for example:
          imageHSV = cv2.cvtColor(imageBGRA[:, :, :3], cv2.COLOR_BGR2HSV)  
          imageHSV[:, :, 2] = cv2.add(imageHSV[:, :, 2], 15)    # increase brightness by 15               
          imageBGRA[:, :, :3] = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)                          

          return imageBGRA
        ```
      Don't forget to import the created method in `app/processors/__init__.py`:

      ```python
      from .your_method import your_method
      ```
      Then you can simply call the created methods in your toolbox:
      
      ```python
      from app import processors
      image = processors.your_method(image)
      ```
---
## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.


