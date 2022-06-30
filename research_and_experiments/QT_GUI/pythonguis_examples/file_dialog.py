import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, 
                                QVBoxLayout,
                                QPushButton, QLabel, QLineEdit,
                                QDialog, QDialogButtonBox)

class CustomDialog(QDialog):

    def __init__(self, parent = None):

        super().__init__(parent) 

        self.value = ""

        self.setWindowTitle("Choose File Window!")

        # buttons: mask that tells QT which one to use
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        # QDialogButtonBox: line of buttons, automatically ordered!
        self.buttonBox = QDialogButtonBox(buttons)
        # signals: they come from the default buttons you inserted!
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        message = QLabel("Something happened, is that OK?")
        self.line_edit= QLineEdit("")

        self.layout.addWidget(message)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)
    
    def get_value(self):
        return self.line_edit.text()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        dialog_button = QPushButton("Open file")
        dialog_button.clicked.connect(self.dialog_button_clicked)

        self.setCentralWidget(dialog_button)


    def dialog_button_clicked(self, s):

        print("dialog button clicked, toggled value: ", s)
        print("opening new dialog window")
        dlg = CustomDialog()
        if dlg.exec_():
            print("Dialog accepted!")
            print(dlg.get_value()) # NOTE: you can store values and retrieve them when the dialog is not in its loop like this!
        else: 
            print("Dialog rejected!")



def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()


if __name__=="__main__":
    main()