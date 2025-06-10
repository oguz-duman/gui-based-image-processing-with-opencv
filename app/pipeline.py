
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
        mask = None                                  # initialize mask to None, it will be used to store the mask produced by steps
        for step in self.steps:
            if step.switch.isChecked():                     # check if the function box is activated
                result = step.execute(image, mask)      
                if isinstance(result, tuple):               # check if the result is a tuple (image, mask)
                    image = result[0]
                    mask = result[1]
                else:
                    image = result
                    mask = None         # this way mask will affect only the following step after the one that produced it
            else:
                mask = None             # if the step is not activated, reset the mask to None in case the previous step produced a mask

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


    def remove_step(self, step_id):
        """
        Remove a step from the pipeline.
        Args:
            step_name (str): The name of the step to be removed from the pipeline.
        """
        for step in self.steps:
            if step.id == step_id:
                self.steps.remove(step)
                break
        
