"""

"""

import sys

from pylsl import StreamInlet, resolve_stream, resolve_byprop, local_clock

from PySide6.QtCore import QStandardPaths, Qt

from PySide6.QtGui import QAction, QIcon

from PySide6.QtWidgets import (
                                QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget,
                                QToolBar, QStatusBar,
                                QLabel, QPushButton, QListWidget, QTreeWidget
                                )


"""
stream selection window
"""
class StreamSelection(QWidget):
    
    def __init__(self):
        super().__init__()
        print("initialising stream selection window...")
        
        self.streams = [] # list of StreamInfo objects
        index = 0
        
        self.label = QLabel("Choose any of the available streams. update list below")
        
        self.stream_list = QListWidget()
        self.stream_list.addItem("Update window to see available outlets. one day, try to make this a tree list!")

        self.update = QPushButton("Update list")
        self.update.clicked.connect(self.find_available_streams)

        self.stream_select = QPushButton("Use selected stream\nNOTE: make sure you set this pressable AFTER selecting a stream, or it will give errors!")
        self.stream_select.clicked.connect(self.set_index)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.stream_list)
        layout.addWidget(self.update)
        layout.addWidget(self.stream_select)
        self.setLayout(layout)

        print("stream selection window initialised.")
    

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
                # for each outlet, also show metadata!
                metadata = "outlet name:\t\t{}\n\ttype:\t\t{}\n\tchannels\t\t{}\n\tsrate\t\t{}\n\tformat\t\t{}\n\tsource id\t\t{}".format(outlet.name() , outlet.type() , outlet.channel_count(), outlet.nominal_srate(), outlet.channel_format(), outlet.source_id())
                self.stream_list.addItem(metadata)

            # print in terminal
            self.print_stream_info(self.streams)

    # helper to the function: find_available_streams
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

    def set_index(self,checked):
        
        items = []
        # make a list of values
        for i in range(self.stream_list.count()):
            items.append( self.stream_list.item(i).text() )
            print(items[i])

        self.index = items.index( self.stream_list.currentItem().text() )
        print("selected index: ", self.index)

        # update main window information thingie: HOW?

        
        

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("A LSL-based GUI")

        """
        ATTRIBUTES
        NOTE: don't use those! use the ones stored in the persisten window "stream_selection_window"
        """
        self.streams = [] # list of available StreamInfo objects holding metadata for LSL stream outlets
        self.metadata = {} # this will hold the outlet metadata as well as additional features like the motor imagery timing and patient data

        """
        PERSISTENT WINDOWS
        """
        self.stream_selection_window = StreamSelection()


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

        self.button_streams = QPushButton("Choose streaming outlet")
        self.button_streams.clicked.connect(self.open_stream_selection_window)

        self.button_experiment = QPushButton("Select experiment type and patient data")
        
        self.label_info = QLabel("Selection parameters will be listed here.\n(!) probably best to use a tree list so you can collapse metadata and experiment data")
        
        self.update_button = QPushButton("update experiment info\n(this button exists because I do not yet know how to synch data between the window I open to the main window)")
        self.update_button.clicked.connect(self.update_label)

        self.button_start = QPushButton("Start experiment (not yet working)")

        layout = QVBoxLayout()
        layout.addWidget(self.button_streams)
        layout.addWidget(self.button_experiment)
        layout.addWidget(self.label_info)
        layout.addWidget(self.update_button)
        layout.addWidget(self.button_start)
        dummy = QWidget()
        dummy.setLayout(layout)

        self.setCentralWidget(dummy)


    def exit_action_called(self):
        self.exit()

    def open_stream_selection_window(self):
        if self.stream_selection_window.isVisible():
            pass
        else:
            self.stream_selection_window.show()

    def update_label(self,checked):
        """
        this only change the contents of the label to show current settings
        """

        self.label_info.clear()
        
        outlet = self.stream_selection_window.streams[ self.stream_selection_window.index ]
        text = "outlet name: \t\t{}\n\ttype: \t{}\n\tchannels\t{}\n\tsrate\t{}\n\tformat\t{}\n\tsource id\t{}".format(outlet.name() , outlet.type() , outlet.channel_count(), outlet.nominal_srate(), outlet.channel_format(), outlet.source_id())

 
        self.label_info.setText(text)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    main_win = MainWindow()

    main_win.show()

    sys.exit(app.exec())




