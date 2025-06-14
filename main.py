import sys, json, os
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow 
from PySide6.QtGui import QPalette, QColor

if __name__ == "__main__":
    app = QApplication([])    


    # Determine the correct path for the palette file
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    palette_path = os.path.join(base_path, "dark_palette.json")

    # Load palette from JSON
    with open(palette_path, "r") as f:
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
