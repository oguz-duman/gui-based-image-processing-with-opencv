import sys, json
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow 
from PySide6.QtGui import QPalette, QColor

if __name__ == "__main__":
    app = QApplication([])    

    # set the application palette from a JSON file
    with open("dark_palette.json", "r") as f:
        palette_dump = json.load(f)

    palette = QPalette()
    for role_name, hex_color in palette_dump.items():
        role = getattr(QPalette.ColorRole, role_name)
        palette.setColor(role, QColor(hex_color))

    app.setPalette(palette)

    # create and show the main window
    widget = MainWindow()     
    widget.resize(800, 600)    
    widget.show()       

    sys.exit(app.exec())        
