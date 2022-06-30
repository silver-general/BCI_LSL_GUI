import sys
import os 
import numpy as np

from pylsl import StreamInlet, resolve_stream, local_clock, StreamInfo

from PySide6.QtCore import QStandardPaths, Qt, QSize

from PySide6.QtGui import QAction, QIcon

from PySide6.QtWidgets import (
                                QApplication, QMainWindow, 
                                QHBoxLayout, QVBoxLayout, QStackedLayout, QFormLayout, QGridLayout, 
                                QWidget, QDialog, QFileDialog,
                                QToolBar, QStatusBar,
                                QLabel, QLineEdit, QPushButton, QListWidget, QTreeWidget, QComboBox, QListWidget
                                )

class CustomWidget(QWidget):
    
    def __init__(self, id = ""):
        super().__init__()

        self.id = id 
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'DATA/MI/STIMULI'))

        
        button = QPushButton("press me for a dialog!")
        button.clicked.connect(self.button_press)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(button)

        self.custom_obj = CustomClass("object01")
    
    
    def button_press(self):
        print("button pressed")
        print("Custom widget id:\t{}".format( self.id))
        #self.browse_image()
        self.custom_obj.browse_image()

    def browse_image(self):
        print("Opening browse stimulus dialog")
        file_name = QFileDialog.getOpenFileName(parent = self, caption = "Browse Audio", dir = self.data_path, filter = "")[0]   

        if len(file_name[0])>0:
            self.picture_path = file_name
            self.description["picture path"] = file_name
            print("a file was selected: ", self.picture_path)
            
        else:
            print("No file was selected")


class CustomClass():
    def __init__(self, id = ""):

        self.id = id
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'example_data'))


    def browse_image(self):
        
        print("opening browse stimulus dialog")

        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'example_data'))
        file_name = QFileDialog.getOpenFileName(parent = None, caption = "Browse Image", dir = self.data_path, filter = "")[0]   

        if len(file_name[0])>0:
            self.picture_path = file_name
            self.description["picture path"] = file_name
            print("a file was selected: ", self.picture_path)
            
        else:
            print("No file was selected") 

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Title")

        self.widg = CustomWidget("widget01")
        self.obj = CustomClass("Object01")

        self.setCentralWidget(self.widg)
    

if __name__ == '__main__':

    app = QApplication(sys.argv)

    main_win = MainWindow()

    main_win.show()

    sys.exit(app.exec())