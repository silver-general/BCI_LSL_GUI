"""https://www.pythonguis.com/tutorials/pyside6-signals-slots-events/"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Slot


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        

        # create button 
        button = QPushButton("Press Me!")
        # make it checkable
        #button.setCheckable(True) 
        # connect its signals: clicked and checked
        button.clicked.connect(self.the_button_was_clicked)
        #button.clicked.connect(self.the_button_was_toggled)
        # set button widget as central
        self.setCentralWidget(button)


    @Slot()
    def the_button_was_clicked(self):
        print("Clicked!")
    @Slot()
    def the_button_was_toggled(self, checked):
        print("Checked?", checked)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()