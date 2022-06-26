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
    QFileDialog
)

from PySide6.QtCore import Qt, QSize, QUrl, QTimer

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
        
        # define a relative path
        self.audio_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'example_data/kitten.wav'))
        print("setting path for data: ", self.audio_path)

        """ using the simple QSoundself.effect https://doc.qt.io/qtforpython/PySide6/QtMultimedia/QSoundself.effect.html """
        self.effect = QSoundEffect()
        self.effect.setSource(QUrl.fromLocalFile(self.audio_path))
        self.effect.setLoopCount(1) # number of times the sound is repeated
            # can also use QSoundEffect.Infinite as parameter!
        self.effect.setVolume(1) # volume ranges 0 to 1 (float)

        layout = QVBoxLayout()

        upload_button = QPushButton("Press to upload pictures")
        upload_button.clicked.connect(self.open_pictures)

        miew_button = QPushButton("Press for a miew!")
        miew_button.clicked.connect(self.play_miew)

        start_slideshow_button = QPushButton("Start Slideshow!")
        start_slideshow_button.clicked.connect(self.start_slideshow)

        form = QFormLayout()
        self.pic_duration = QLineEdit()
        form.addRow("pic duration", self.pic_duration)

        self.pic_list = []
        self.picture = QLabel() # used as cat.setPixmap(QPixmap("cat.png"))
        
        layout.addWidget(upload_button)
        layout.addLayout(form)
        layout.addWidget(miew_button)
        layout.addWidget(start_slideshow_button)
        layout.addWidget(self.picture)

        dummy = QWidget()
        dummy.setLayout(layout)

        self.setCentralWidget(dummy)

    def play_miew(self):
        print("playing sound!")
        self.effect.play()
    
    def open_pictures(self):
        file_dialog = QFileDialog(self)
        data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'example_data/'))
        # NOTE: the function returns a tuple, and the first element is the chosen path! second is the filters used. QUESTION why do this?
        file_names = QFileDialog.getOpenFileNames(parent = self, caption = "Open File", dir = data_path, filter = "")[0]   
            # is this a list of paths?
        print("selecting pictures: ", file_names)
        print(type(file_names))

        #self.picture.setPixmap(QPixmap(file_names[0]))
        self.pic_list = file_names

    def start_slideshow(self):
        print("starting slideshow")
        print("picture duration", self.pic_duration.text())

        timer = QTimer()
        timer.setInterval(msec = self.pic_duration.text()) # https://doc.qt.io/qtforpython/PySide6/QtCore/QTimer.html#PySide6.QtCore.PySide6.QtCore.QTimer.setInterval
        timer.singleShot()

        for pic in self.pic_list:
            self.picture.setPixmap(QPixmap(pic))

    def timer_event(self):
        # quen timer's up, update picture and slideshow index
        pass



if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())