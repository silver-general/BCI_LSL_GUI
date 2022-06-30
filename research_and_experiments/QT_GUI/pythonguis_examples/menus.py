"""https://www.pythonguis.com/tutorials/pyside6-actions-toolbars-menus/"""

import sys
from PySide6.QtWidgets import ( QMainWindow, QApplication, QLabel, QToolBar, QStatusBar )
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt
from PySide6.QtCore import Slot
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My Awesome App")

        """create a label, center it, and add it to the main window"""
        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

        """create a toolbar object, add it to the main window"""
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        """action: 
        - create action object with a name
        - set status tip
        - when triggered, connect the signal to a function of the main window
        - add the action to the toolbar
        """
        button_action = QAction("Your button", self) # NOTE: self passed as final parameter!
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(button_action)

    """method: when user clocks on toolbar element"""
    @Slot()
    def onMyToolBarButtonClick(self, s):
        print("click", s) # why does it return false?


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()

