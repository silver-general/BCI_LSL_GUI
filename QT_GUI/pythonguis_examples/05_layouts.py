"""
HOW TO ADD A LAYOUT
    create a layout
    add widgets to it
    create dummy widget
    add layout to dummy widget
    set dummy widget in the main window (or wherever you want)

SPACING AND MARGINS IN A LAYOUT
    layout = some QT layout type
    layout.setContentsMargins(0,0,0,0)
    layout.setSpacing(20)

4 BASIC LAYOUTS
    QHBoxLayout 	Linear horizontal layout
    QVBoxLayout 	Linear vertical layout
    QGridLayout 	In indexable grid XxY
    QStackedLayout 	Stacked (z) in front of one another

NESTING LAYOUTS
    create internal layout and set it up
    create external ..
    add internal layout to external layout (no dummy widget required, just use .addLayout(). see below!)
    use dummy widget, assign external layout, set dummy wherever you want

TODO: GRID AND STACKED LAYOUTS! https://www.pythonguis.com/tutorials/pyside6-layouts/
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout,QVBoxLayout,QGridLayout,QStackedLayout
from PySide6.QtGui import QPalette, QColor

"""
custom widget
    a widget whose background colour is decided at its instantiation
"""
class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("My App")   
        
        """
        example: instantiating the example widget
        """
        box_01 = Color("red")        
        self.setCentralWidget(box_01)

        """
        QVBoxLayout: vertical layout
        """
        layout_vert = QVBoxLayout() 

        layout_vert.addWidget(Color('red'))
        layout_vert.addWidget(Color('green'))
        layout_vert.addWidget(Color('blue'))

        dummy = QWidget()
        dummy.setLayout(layout_vert)
        self.setCentralWidget(dummy)

        """
        QHBoxLayout: horizontal
            NOTE: same declaration as the horizontal, widgets arranged differently!
        """
        layout_hor = QHBoxLayout() 

        layout_hor.addWidget(Color('red'))
        layout_hor.addWidget(Color('green'))
        layout_hor.addWidget(Color('blue'))

        dummy = QWidget()
        dummy.setLayout(layout_hor)
        self.setCentralWidget(dummy)

        """
        NESTING LAYOUTS
        
            let's try to have an horizontal layout of 3, with the second widget containing a layout of 3 vertical widgets!
        """
        # inner layout: vertial, 3 widgets
        layout_01 = QVBoxLayout()
        layout_01.addWidget(Color("red"))
        layout_01.addWidget(Color("green"))
        layout_01.addWidget(Color("blue"))
        # NOTE: dummy for the inner layout: no need, just add internal layout to external layout!
        
        layout_00 = QHBoxLayout()
        layout_00.addWidget(Color("purple"))
        layout_00.addLayout(layout_01) # same NOTE: dummy for the inner layout: no need, just add internal layout to external layout!

        # create dummy to hold all
        dummy = QWidget()
        # assign final layout to dummy
        dummy.setLayout(layout_00)
        # assign dummy to central widget
        self.setCentralWidget(dummy)

        """
        GRID LAYOUT STACKED LAYOUTS: DON'T NEED THE NOW. https://www.pythonguis.com/tutorials/pyside6-layouts/
        """

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()















