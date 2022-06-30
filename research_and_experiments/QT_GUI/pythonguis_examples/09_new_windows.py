"""
https://www.pythonguis.com/tutorials/pyside6-creating-multiple-windows/

any widget without a parent is opened as a new window

when you create a widget, you need to .show() it
"""



from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.label = QLabel("Another Window")

        layout.addWidget(self.label)

        self.setLayout(layout)




class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.newwindow = None



        """
        CREATING A PERSISTENT WINDOW
            it's a window you define here, and then you show/unshow later using
                .show() or .hide() checking .isVisible() method
        """
        self.pers_window = AnotherWindow()
        
        """
        create layout elements
        """
        # this shows a non-persistent window
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        
        # this handles a persistent window
        self.button_02 = QPushButton("show/hide persistent window")
        self.button_02.clicked.connect(self.show_hide)

        # assemble layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.button_02)
        
        dummy = QWidget()
        dummy.setLayout(layout)
        self.setCentralWidget(dummy)


    def show_new_window(self, checked):
        """
        NOTE: you need to keep a reference to this new window, so you create an attribute for the parent to keep it's reference!
        NOTE: this will e run everytime you press the button in the mainwindow!
        NOTE: to handle the reference, check the mainwindow attribute status
        NOTE: if you close the window, the reference will stay there and not be deleted!
        """
        print("button pushed")
        if self.newwindow == None: # if there is no reference to a new window, create one
            print("creating new window")
            self.newwindow = AnotherWindow()
            self.newwindow.show()
        else: # if there a reference, don't do anything
            print("window already existing. closing it.")
            self.newwindow.close()
            self.newwindow = None
            
    def show_hide(self, checked):
        if self.pers_window.isVisible():
            self.pers_window.hide()
        else:
            self.pers_window.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()

