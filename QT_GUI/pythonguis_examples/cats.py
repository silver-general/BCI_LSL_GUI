import sys
import os
from random import randint
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit, QPushButton,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider,
    QLayout, QHBoxLayout
)

from PySide6.QtCore import Qt, QSize, QUrl

from PySide6.QtMultimedia import (QAudio, QAudioOutput, QMediaFormat, QMediaPlayer, QSoundEffect)

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

        """ AUDIO """
        self._audio_output = QAudioOutput()
        self._player = QMediaPlayer()
            # NOTE: to play music: self._player.play()
            # NOTE: to pause music: self._player.pause()
            # NOTE: to stop: self._player.stop()
            # NOTE: to setup source:  self._player.setSource(self._playlist[self._playlist_index]) 
        self._player.setAudioOutput(self._audio_output)

        """using a low latency sound effect
        read: https://doc.qt.io/qtforpython/PySide6/QtMultimedia/QSoundEffect.html
        """
        miew_sound = QSoundEffect()
        miew_sound.setSource(QUrl.fromLocalFile("Kitten_Meow.wav"))
        miew_sound.setLoopCount(QSoundEffect.Infinite)
        miew_sound.setVolume(100)
        miew_sound.playingChanged.connect(print("playing changed!"))
        miew_sound.play()
        print("initialised main window")

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
