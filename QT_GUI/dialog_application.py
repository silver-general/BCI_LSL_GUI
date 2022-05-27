"""
- user can input name
- user can push button
- application greets the user
"""

import sys
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton
from PySide6.QtWidgets import QVBoxLayout
"""
create a custom dialog that we call Form, and inherits from the QDialog class
"""
class Form(QDialog):

    def __init__(self, parent=None):
        # calls for the parent's init, if there is any
        super(Form, self).__init__(parent)
        # sent the title of the window
        self.setWindowTitle("My Form")

        # Create widgets
        self.edit = QLineEdit("Write your name here..")
        self.button = QPushButton("Show Greetings")

        # Create layout and add widgets
        layout = QVBoxLayout(self)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

        # connect widgets. self.button.clocked() signal to self.greeting() method
        self.button.clicked.connect(self.greetings)
        
    # method: Greets the user
    def greetings(self):
        print("hello {}".format( self.edit.text() ) )
        self.button.setText("hello {}".format(self.edit.text()))


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())
