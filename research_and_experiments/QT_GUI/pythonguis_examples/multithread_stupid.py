""" TUTORIAL: https://www.pythonguis.com/tutorials/multithreading-pyside6-applications-qthreadpool/ """

from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget, QMainWindow, QApplication
from PySide6.QtCore import QTimer

import sys
import time

class MainWindow(QMainWindow):


    def __init__(self):
        super(MainWindow, self).__init__()

        self.counter = 0 #timer counter

        layout = QVBoxLayout()

        self.l = QLabel("Start") # starts loop
        b = QPushButton("DANGER!") # blocks execution of main thread entirely
        b.pressed.connect(self.oh_no)

        layout.addWidget(self.l)
        layout.addWidget(b)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

        self.timer = QTimer() # timer that will print its counter every second (like an interrupt)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def oh_no(self):
        
        # time.sleep(5)
        """
        instead of blocking everything, process events everysecond so that the main thread becomes responsive (sort of)
        """
        for n in range(5):
            QApplication.processEvents()
            time.sleep(1)

    def recurring_timer(self): 
        self.counter +=1
        self.l.setText("Counter: %d" % self.counter)


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()