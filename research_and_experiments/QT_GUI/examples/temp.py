"""
GENERAL IMPORTS
"""
import sys 

"""
QT ENVIRONMENT
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QLabel, QDockWidget
from PySide6.QtGui import QIcon, QAction 
    # Qicon to setup icons
    # Qaction to setup actions such as exiting when selecting exit from the file dropdown menu 
        # READ THIS! https://doc.qt.io/qt-5/qaction.html#details
from PySide6.QtCore import Slot

# I will need a button to scan for streams

"""
LABSTREAMING LAYER
"""
from pylsl import StreamInlet, resolve_stream, resolve_byprop, local_clock



"""
MAIN WINDOW
"""
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Alberto's App")

        # keep a dictionary of settings just in case
        self.settings = {}

        """ adding a toolbar """
        # create and add a toolbar to main window
        tool_bar = QToolBar()
        self.addToolBar(tool_bar)

        """ file menu """
        # add a "file" dropdown menu to the main window (default) menu bar
        file_menu = self.menuBar().addMenu("&File")

        # add an "exit" action into the file menu
        icon = QIcon.fromTheme("application-exit")

        # create an action to add to the file menu: "exit"
        exit_action = QAction(icon, "E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
            # when triggered, runs self.close(). see https://doc.qt.io/qtforpython/PySide6/QtWidgets/QWidget.html#PySide6.QtWidgets.PySide6.QtWidgets.QWidget.close
        file_menu.addAction(exit_action)

        """stream menu"""
        # add a "streams" dropdown menu
        streams_menu = self.menuBar().addMenu("&Streams")

        # create an action to add to the file menu: "exit"
        find_streams_action = QAction(icon, "Find streams", self, shortcut="", triggered=self.find_streams)
        # when triggered, runs ...
        streams_menu.addAction(find_streams_action)

        """adding a central widget """

        
        


        """ adding a label for communication """
        #this is in the lower dock of main window

        """ LSL streams """
        self.streams = []

    """functions that handle finding outlets"""
    @Slot()
    def find_streams(self):
        print("finding all available streams.")
        self.streams = resolve_stream()
    @Slot()
    def print_streams():

        for i in range(len(self.streams())):
            print(  "outlet {}"             .format(i)                                  )
            print(  "\tname:\t\t{}"         .format(streams[i].name())                  )
            print(  "\ttype:\t\t{}"         .format(streams[i].type())                  ) 
            print(  "\t#_channels:\t{}"     .format(streams[i].channel_count())         )
            print(  "\ts_rate:\t\t{}"       .format(streams[i].nominal_srate())         )
            print(  "\tdtype:\t\t{}"        .format(streams[i].channel_format())        )
            print(  "\tID:\t\t{}"           .format(streams[i].source_id())             )
    @Slot()
    def message():
        label.text()
    """miscellaneousfunctions"""
    @Slot()
    def debug(self,message="the thing you wanted, it happened"):
        """
        just run this wherever you wanna see something happening
        """
        print(message)
        return




""" stream selection class """
#class StreamSelection

def main():
    print("executing main()!")

    app = QApplication(sys.argv)

    # define main window and geometry
    main_win = MainWindow()
    available_geometry = main_win.screen().availableGeometry()
    main_win.resize(available_geometry.width() / 3,
                    available_geometry.height() / 2)
    main_win.show()
    
    # what does this do exactly?
    sys.exit(app.exec())



if __name__=="__main__":
    main()