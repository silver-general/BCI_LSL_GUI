import sys
from random import randint
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit, QPushButton,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider,
    QLayout, QHBoxLayout
)
from PySide6.QtCore import Qt, QSize

from PySide6.QtGui import QPixmap,QIcon

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.cat_number = 0
        self.windows = []

        self.setWindowTitle("My App")
        

        label = QLabel("select number of cats")

        spin = QSpinBox()
        spin.setMinimum(0)
        spin.valueChanged.connect(self.setcatnumber)

        button = QPushButton(QIcon("cat.png"), "press to generate kittens")
        button.clicked.connect(self.showcats)

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(spin)
        layout.addWidget(button)

        dummy = QWidget()
        dummy.setLayout(layout)

        self.setCentralWidget(dummy)

    def setcatnumber(self, number):
        self.cat_number = number
        print("current cat number: ",int(number))

    def showcats(self, checked):
        print("generating {} cats".format(self.cat_number))
        for i in range(self.cat_number):
            # create a new window and show ignorantly
            cat = QLabel()
            cat.setPixmap(QPixmap("cat.png"))
            cat.setGeometry(randint(1,10)*100,randint(1,5)*50,800,800)
            cat.show()
            self.windows.append(cat)

"""app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
"""

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
