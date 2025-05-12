
class Pipeline():
    def __init__(self):
        self.steps = []
        

    def add_step(self, step):
        """
        Add a step to the pipeline.
        """
        self.steps.append(step)

    def run(self, image):
        """
        Run the pipeline on the input image.
        """

        for step in self.steps:
            # check if the function box is activated
            if step.switch.isChecked():
                image = step.execute(image)             # call the process function of the function box
        
        return image                # make a copy of the processed image for output



    def clear(self):
        """
        Clear the pipeline.
        """
        self.steps = []

    def move_step(self, step, new_index):
        """
        Move a step to a new index in the pipeline.
        """
        
        # Check if the widget is in the pipeline
        if step in self.steps:
            # Remove the widget from its current position in the pipeline
            self.steps.remove(step)
            # Insert the widget at the new index in the pipeline
            self.steps.insert(new_index, step)


    def remove_step(self, step_name):
        """
        Remove a step from the pipeline.
        """
        for step in self.steps:
            if step.title == step_name:
                self.steps.remove(step)
                break
        
