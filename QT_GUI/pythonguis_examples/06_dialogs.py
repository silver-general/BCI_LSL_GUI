"""
DIALOG
    small modal (blocks access to other windows) window used to communicate with user
    class: QDialog

    to create a dialog
        you need to pass a parent window!
        NOTE: you create an entirely new event loop when you run its exec method!
    to personalise a dialog: create a custom dialog that inherits from QDialog


    MESSAGEBOX: read mode https://www.pythonguis.com/tutorials/pyside6-dialogs/ later
"""

import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout,QDialogButtonBox,QLabel, QMessageBox

"""
custom dialog
"""
class CustomDialog(QDialog): 
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HELLO!")

        """
        CREATING A BUTTON BOX
            you can OR or "|" different buttons
            choose from buttons
                    QDialogButtonBox.Ok
                    QDialogButtonBox.Open
                    QDialogButtonBox.Save
                    QDialogButtonBox.Cancel
                    QDialogButtonBox.Close
                    QDialogButtonBox.Discard
                    QDialogButtonBox.Apply
                    QDialogButtonBox.Reset
                    QDialogButtonBox.RestoreDefaults
                    QDialogButtonBox.Help
                    QDialogButtonBox.SaveAll
                    QDialogButtonBox.Yes
                    QDialogButtonBox.YesToAll
                    QDialogButtonBox.No
                    QDialogButtonBox.Abort
                    QDialogButtonBox.Retry
                    QDialogButtonBox.Ignore
                    QDialogButtonBox.NoButton
        """
        # NOTE: investigate what this does exactly!
            # this is a "flag" of buttons to pass to the dialog button instantiation!
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel 

        # instance dialog box, pass the button mask!
        self.buttonBox = QDialogButtonBox(QBtn)

        self.buttonBox.accepted.connect(self.accept) # when you click ok
        self.buttonBox.rejected.connect(self.reject) # when you click cancel

        # put buttons in a layout, hold a message above and buttons below
        self.layout = QVBoxLayout()

        message = QLabel("Something happened, is that OK?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)

        # set layout in this very widget
        self.setLayout(self.layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press me for a dialog!")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, s):
        print("click", s)
        dlg = CustomDialog()
        dlg.setWindowTitle("HELLO!")
        dlg.exec_()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()

