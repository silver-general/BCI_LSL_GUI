import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")


        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.button_clicked())

        self.setCentralWidget(self.button)

        # use an attribute to keep track of state of widgets
        self.button_status = True

        # create a button
        self.button = QPushButton("Press Me!")
        # make it capable of toggling
        self.button.setCheckable(True)

        # signal: if button clicked, say that
        self.button.clicked.connect(self.button_clicked)
        # signal: if button is toggled, say that. the slot function an also take a status, "check"
        self.button.clicked.connect(self.button_toggled)

        # Set the central widget of the Window.
        self.setCentralWidget(self.button)
    
    
    def button_clicked(self):
        print("Clicked!")
        self.button.setText("You already clicked me.")
        self.button.setEnabled(False)
        
    def button_toggled(self,checked):
        print("toggled: ",checked)
        self.button_status = checked

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()

