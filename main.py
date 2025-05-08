import sys
from PySide6.QtWidgets import QApplication

from ui.main_widget import MainWidget 

if __name__ == "__main__":
    app = QApplication([])    

    widget = MainWidget()     
    widget.resize(800, 600) 
    widget.show()       

    sys.exit(app.exec())        
