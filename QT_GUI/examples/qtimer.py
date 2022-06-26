import sys
import os
from random import randint
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

        
        # define a relative path
        self.audio_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'example_data/kitten.wav'))
        print("setting path for data: ", self.audio_path)

        """ using the simple QSoundself.effect https://doc.qt.io/qtforpython/PySide6/QtMultimedia/QSoundself.effect.html """
        self.effect = QSoundEffect()
        self.effect.setSource(QUrl.fromLocalFile(self.audio_path))
        self.effect.setLoopCount(1) # number of times the sound is repeated
            # can also use QSoundEffect.Infinite as parameter!
        self.effect.setVolume(1) # volume ranges 0 to 1 (float)

        """ SETUP TIMER """
        timer = QTimer(self) 
        timer.timeout.connect(self.play_miew)

        timer.start(1000)


        layout = QVBoxLayout()

        miew_button = QPushButton("Press for a miew!")
        miew_button.clicked.connect(self.play_miew)

        form = QFormLayout()
        self.duration = QLineEdit()
        form.addRow("timer timeout", self.duration)

        self.picture = QLabel()
        
        layout.addLayout(form)
        layout.addWidget(miew_button)
        layout.addWidget(self.picture)

        dummy = QWidget()
        dummy.setLayout(layout)

        self.setCentralWidget(dummy)
    

    def play_miew(self):
        """
        plays sounds based on a timer
        """
        print(self.duration.text())
        self.effect.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())