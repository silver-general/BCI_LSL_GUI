import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # setup window name and size
        self.setWindowTitle("My App")
        self.setFixedSize(QSize(400, 300))

        button = QPushButton("Press Me!")
        button.clicked.connect(self.say_hi)

        # Set the central widget of the Window.
        self.setCentralWidget(button)

        # set the manubar
        menu = QMen
        self.setMenuWidget(menubar)
    def say_hi(self):
        print("hi!")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()