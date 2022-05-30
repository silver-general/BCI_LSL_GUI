"""

"""

import sys

from pylsl import StreamInlet, resolve_stream, resolve_byprop, local_clock

from PySide6.QtCore import QStandardPaths, Qt

from PySide6.QtGui import QAction, QIcon

from PySide6.QtWidgets import (
                                QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget,
                                QToolBar, QStatusBar,
                                QLabel, QPushButton, QListWidget
                                )



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("A LSL-based GUI")

        """
        ATTRIBUTES
        """
        self.streams = [] # list of available StreamInfo objects holding metadata for LSL stream outlets


        """
        STATUS BAR
            QStatusBar
            .setStatusBar run from main window
            displays status
            settings:
                ...
        """
        status = QStatusBar(self)
        self.setStatusBar(status)

        """
        PERSISTENT WINDOWS
            MAYBE? stream list: always keep it in case you wanna see it
        """
        ...


        """
        MENU
        """
        menu = self.menuBar()

        file_menu = menu.addMenu("File")
        file_menu.addSeparator()

        """add something to the file menu, like an exit option (an action)"""
        exit_action = QAction(QIcon.fromTheme("application-exit"),"Quit", self) # first, define an action  
        exit_action.triggered.connect(self.exit_action_called)      
        file_menu.addAction(exit_action)


        """
        LAYOUT
        """
        # first, setup elements
        self.label = QLabel("available streams (update with button below): ")
        
        self.stream_list = QListWidget()
        
        self.resolver = QPushButton("Update available streams")
        self.resolver.clicked.connect(self.find_available_streams)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.stream_list)
        layout.addWidget(self.resolver)

        dummy = QWidget()
        dummy.setLayout(layout)

        self.setCentralWidget(dummy)



    def exit_action_called(self):
        self.exit()


    """
    LSL RELATED THINGS
    """


    def find_available_streams(self):
        """
        finds all streams. 
        """
        print("finding available outlets...\n")
        streams = resolve_stream()
        ##print_streams_info(streams)

        if len(streams)==0:
            print("no outlets found!")
            # update streamInfo objects list
            self.streams = []
            # update QListWidget elements
            self.stream_list.clear()
            self.stream_list.addItem("no outlets found!")


        else:
            print("all stream outlets selected")

            # update list of StreamInfo metadata
            self.streams = streams
            
            # update QListWidget: delete old entries and add new ones
            self.stream_list.clear()
            for outlet in streams:
                self.stream_list.addItem(outlet.name())

            # print in terminal
            self.print_stream_info(self.streams)


    def print_stream_info(self, streams):
        """
        prints the StreamInfo information of a list of outlets
        NOTE: DECIDE IF YOU WANT THIS TO BE A METHOD OR STANDALONE FUNCTION!
        """
        for i in range(len(streams)):
            print(  "outlet {}"             .format(i)                                  )
            print(  "\tname:\t\t{}"         .format(streams[i].name())                  )
            print(  "\ttype:\t\t{}"         .format(streams[i].type())                  ) 
            print(  "\t#_channels:\t{}"     .format(streams[i].channel_count())         )
            print(  "\ts_rate:\t\t{}"       .format(streams[i].nominal_srate())         )
            print(  "\tdtype:\t\t{}"        .format(streams[i].channel_format())        )
            print(  "\tID:\t\t{}"           .format(streams[i].source_id())             )



if __name__ == '__main__':

    app = QApplication(sys.argv)

    main_win = MainWindow()

    main_win.show()

    sys.exit(app.exec())