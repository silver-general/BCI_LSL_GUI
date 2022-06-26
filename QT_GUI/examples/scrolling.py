"""
I will try a manual slideshow where I keep track of time and 
    show pictures using the QPixmap https://doc.qt.io/qtforpython/PySide6/QtGui/QPixmap.html
    play audio using the QAudio https://doc.qt.io/qtforpython-6/PySide6/QtMultimedia/QAudio.html

    timing: use QTimer https://doc.qt.io/qtforpython/PySide6/QtCore/QTimer.html
"""


import sys
import os
from random import randint
from pylsl import local_clock
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit, QPushButton,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider,
    QLayout, QHBoxLayout, QVBoxLayout, QFormLayout,
    QFileDialog,
    QScrollArea, QSizePolicy
)

from PySide6.QtCore import Qt, QSize, QUrl, QTimer

from PySide6.QtMultimedia import (QAudio, QAudioOutput, QMediaFormat, QMediaPlayer, QSoundEffect)

from PySide6.QtGui import QPixmap,QIcon, QPalette

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # define a relative path
        self.path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'example_data/kitten.png'))
        print("setting path for data: ", self.path)


        layout = QVBoxLayout()

        inner_layout = QVBoxLayout()

        label = QLabel("hello I am a label for the picture")
 

        picture = QLabel() # used as cat.setPixmap(QPixmap("cat.png"))
        picture.setPixmap(QPixmap(self.path))
        picture.setBackgroundRole(QPalette.Base)
        picture.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored) 
            # this makes the image reshapable
        picture.setScaledContents(True)

        inner_layout.addWidget(label)
        inner_layout.addWidget(picture)



        scroll_area = QScrollArea()
        scroll_area.setBackgroundRole(QPalette.Dark)
        # scroll_area.setWidget(picture)

        ##layout.addWidget(scroll_area)
        layout.addLayout(inner_layout)

        dummy = QWidget()
        dummy.setLayout(layout)

        scroll_area.setWidget(dummy)

        self.setCentralWidget(scroll_area)




if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    available_geometry = window.screen().availableGeometry()
    window.resize(available_geometry.width() / 6, available_geometry.height() / 4)
    window.show()
    sys.exit(app.exec_())