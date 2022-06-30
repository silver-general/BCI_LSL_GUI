import sys
import os
from random import randint
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit, QPushButton,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider,
    QLayout, QHBoxLayout, QVBoxLayout
)

from PySide6.QtCore import Qt, QSize, QUrl

from PySide6.QtMultimedia import (QAudio, QAudioOutput, QMediaFormat, QMediaPlayer, QSoundEffect)

from PySide6.QtGui import QPixmap,QIcon

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()


        """ AUDIO 
            # NOTE: to play music: self.player.play()
            # NOTE: to pause music: self.player.pause()
            # NOTE: to stop: self.player.stop()
            # NOTE: to setup source:  self.player.setSource(self._playlist[self._playlist_index]) 
        """

        """ USING QMediaPlayer"""
        # main object to handle media playing
        self.player = QMediaPlayer()

        # default audio output, or pass as parameter the one you want
        self.audio_output = QAudioOutput()

        # assign audio output to QMediaPlayer
        self.player.setAudioOutput(self.audio_output)
        
        # define a relative path
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'example_data/kitten.wav'))
        print("setting path for data: ", self.data_path)

        # assign source to play 
        self.player.setSource(QUrl.fromLocalFile(self.data_path))

        """ using the simple QSoundself.effect https://doc.qt.io/qtforpython/PySide6/QtMultimedia/QSoundself.effect.html """
        self.effect = QSoundEffect()
        self.effect.setSource(QUrl.fromLocalFile(self.data_path))
        self.effect.setLoopCount(1) # number of times the sound is repeated
            # can also use QSoundEffect.Infinite as parameter!
        self.effect.setVolume(1) # volume ranges 0 to 1 (float)
        

        layout = QVBoxLayout()
        button = QPushButton("Press for a miew!")
        button.clicked.connect(self.play_miew)

        layout.addWidget(button)

        dummy = QWidget()
        dummy.setLayout(layout)

        self.setCentralWidget(dummy)

    def play_miew(self):
        print("playing sound!")
        ##self.player.play()
        self.effect.play()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())