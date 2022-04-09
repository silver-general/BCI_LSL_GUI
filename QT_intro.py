"""
check pySide6 version
"""

import PySide6.QtCore

# Prints PySide6 version
print(PySide6.__version__)

# Prints the Qt version used to compile PySide6
print(PySide6.QtCore.__version__)


"""
first application
"""
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel
                                                    
if __name__ == "__main__":

    app = QApplication(sys.argv)
    label = QLabel("Hello World", alignment=Qt.AlignCenter)
    label.show()
    sys.exit(app.exec_())


"""
second simple application
https://doc.qt.io/qtforpython/quickstart.html
"""
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.magic)
    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    # NOTE: check if there is an instance already present
    # read https://stackoverflow.com/questions/50005373/runtimeerror-please-destroy-the-qapplication-singleton-before-creating-a-new-qa
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())


