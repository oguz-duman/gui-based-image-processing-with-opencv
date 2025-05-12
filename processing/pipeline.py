
class Pipeline():
    """
    A class representing a processing pipeline for image processing.
    The pipeline consists of a series of steps, each represented by a FunctionBox class.
    """
    def __init__(self):
        self.steps = []       
        

    def add_step(self, step):
        """
        Add a step to the pipeline.
        Args:
            step (FunctionBox class): The step to be added to the pipeline.
        """
        self.steps.append(step)


    def run(self, image):
        """
        Run the pipeline on the input image.
        Args:
            image (numpy array): The input image to be processed in the BGRA format.
        Returns:
            image (numpy array): The processed image in the BGRA format.
        """
        for step in self.steps:
            # check if the function box is activated
            if step.switch.isChecked():
                image = step.execute(image)           
        return image              


    def clear(self):
        """
        Clear the whole pipeline.
        """
        self.steps = []


    def move_step(self, step, new_index):
        """
        Move a step to a new index in the pipeline.
        Args:
            step (FunctionBox Class): The step to be moved in the pipeline.
            new_index (int): The new index to move the step to in the pipeline.
        """
        if step in self.steps:
            self.steps.remove(step)                     # Remove the widget from its current position
            self.steps.insert(new_index, step)          # Insert the widget at the new index in the pipeline


    def remove_step(self, step_name):
        """
        Remove a step from the pipeline.
        Args:
            step_name (str): The name of the step to be removed from the pipeline.
        """
        for step in self.steps:
            if step.title == step_name:
                self.steps.remove(step)
                break
        
