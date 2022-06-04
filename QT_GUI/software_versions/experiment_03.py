"""
VERSION 2

NOW I HAVE A LAYOUT WITH CENTRAL WIDGET
    dividen in 2
        left: vertical bar with writings "select stream", "select patient data", "select experiment type"
"""


import sys

from pylsl import StreamInlet, resolve_stream, local_clock, StreamInfo

from PySide6.QtCore import QStandardPaths, Qt

from PySide6.QtGui import QAction, QIcon

from PySide6.QtWidgets import (
                                QApplication, QMainWindow, 
                                QHBoxLayout, QVBoxLayout, QStackedLayout, QFormLayout, 
                                QWidget, QDialog,
                                QToolBar, QStatusBar,
                                QLabel, QLineEdit, QPushButton, QListWidget, QTreeWidget, QComboBox
                                )



class StreamSelectionWindow(QWidget):
    """
    open this with self.show_stream_selection_window() method
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stream Selection")

        self.streams = [] # THIS IS THERE THE StreamInfo OBJECTS ARE!!
        self.index = 0
        
        self.layout = QVBoxLayout()

        self.stream_list = QListWidget()
        self.stream_list.addItem("Please update list of streams")
        self.stream_list.currentItemChanged.connect(self.update_index)

        self.update = QPushButton("Update list of streams")
        self.update.clicked.connect(self.scan_streams)

        self.accept = QPushButton("Accept selected stream")
        ##self.accept.clicked.connect(self.accept_stream_and_close)

        self.close_window = QPushButton("Close")
        
        self.layout.addWidget(self.stream_list)
        self.layout.addWidget(self.update)
        self.layout.addWidget(self.accept)
        self.layout.addWidget(self.close_window)

        self.setLayout(self.layout)

    def update_index(self):

        self.index = self.stream_list.currentRow()
        ###print("selection changed: ", self.index)

    def scan_streams(self):
        streams = resolve_stream()
        print("looking for streams.")
        self.print_streams_info(streams)

        self.streams = streams

        # add stream info names to list
        self.stream_list.clear()
        for outlet in streams:
            metadata = "outlet name:\t\t{}\n\ttype:\t\t{}\n\tchannels\t\t{}\n\tsrate\t\t{}\n\tformat\t\t{}\n\tsource id\t\t{}".format(outlet.name() , outlet.type() , outlet.channel_count(), outlet.nominal_srate(), outlet.channel_format(), outlet.source_id())
            self.stream_list.addItem(metadata)

    def accept_stream_and_close(self):
        """
        NOTE: this is note used, as there is a function in the main window that takes care of getting the metadata and closing!!!!!!!!!!!!!!!!!!! IS HIS CORRECT?
        """
        print("accepting stream and closing")
        self.close()

    def print_streams_info(self, streams):
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

# make this into a dialog? QUESTION
class ExperimentSetupWindow(QWidget):
    """
    open this with self.show_experiment_setup_window() method
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Experiment Type Setup")
        
        self.experiment_info = {"Experiment Type" : "No experiment selected"} # QUESTION: sshould I even use those? i can directly update the main window metadata!
        self.MI_parameters = {}
        self.SSVEP_parameters = {}

        self.accept_selection = QPushButton("Accept Selection")
        self.close_window = QPushButton("Close")
        self.close_window.clicked.connect(self.close)
        

        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create and connect the combo box to switch between pages
        self.page_combo = QComboBox()
        self.page_combo.addItems(["No Experiment Selected", "Motion Imagery", "SSVEP (not yet vailable)"])

        self.page_combo.activated.connect(self.switchPage)

        # Create the stacked layout
        self.stackedLayout = QStackedLayout()

        # Create the page in the case of no selection
        self.page0 = QLabel("Select Experiment type first")

        self.stackedLayout.addWidget(self.page0)

        # Create the second page
        self.page1 = QWidget()

        self.page1Layout = QFormLayout()

        # for practice, create a list of widgets to use in the form layout
        self.stimulus_duration = QLineEdit()
        self.rest_time = QLineEdit()
        self.runs_per_class = QLineEdit() # number of runs for each image

        self.page1Layout.addRow("Stimulus duration:", self.stimulus_duration)
        self.page1Layout.addRow("Rest time", self.rest_time)
        self.page1Layout.addRow("Number of runs per stimulus", self.runs_per_class)

        self.page1.setLayout(self.page1Layout)

        self.stackedLayout.addWidget(self.page1)

        # Create the third page
        self.page2 = QWidget()
        self.page2_layout = QFormLayout()
        self.page2_layout.addRow("Parameter 1", QLineEdit())
        self.page2_layout.addRow("Parameter 2", QLineEdit())

        self.page2.setLayout(self.page2_layout)

        self.stackedLayout.addWidget(self.page2)


        # Add the combo box and the stacked layout to the top-level layout
        layout.addWidget(self.page_combo)
        layout.addLayout(self.stackedLayout)
        layout.addWidget(self.accept_selection)
        layout.addWidget(self.close_window)

    def switchPage(self):

        self.stackedLayout.setCurrentIndex(self.page_combo.currentIndex())

    def selection_changed(self):
        print("Experiment selection changed: ")
        print(self.experiment_type.currentIndex())
        print(self.experiment_type.currentText())


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("A LSL-based GUI")

        """
        ATTRIBUTES: METADATA
        NOTE: decide whether to use those or the ones stored in the persisten window "stream_selection_window"
        """
        self.stream_info = [] # list of available StreamInfo objects holding metadata for LSL stream outlets
        self.selected_stream = 0 # reference to the selected stream in self.stream_info list

        self.patient_data = {} # this will hold the outlet metadata as well as additional features like the motor imagery timing and patient data
        self.experiment_info = {"Experiment Type" : "No experiment selected"}

        """
        PERSISTENT WINDOWS
        """
        ##self.stream_selection_window = StreamSelectionWindow()
        ##self.MI_settings_window = MotionImagerySettingWindow()

        self.stream_selection = StreamSelectionWindow()
        self.stream_selection.accept.clicked.connect(self.set_stream) # this is the magic: connect a button from the child window to a method in the parent window!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.stream_selection.close_window.clicked.connect(self.close_stream_selection_window)

        self.experiment_setup_window = ExperimentSetupWindow()
        self.experiment_setup_window.accept_selection.clicked.connect(self.set_experiment_type)


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
        #
        tools_menu = menu.addMenu("Tools")
        #
        streams_menu = tools_menu.addMenu("Streams")

        view_streams_action = QAction("View/Select available streams",self)
        ##view_streams_action.triggered.connect(self.open_stream_selection_window)

        streams_menu.addAction(view_streams_action)
        #
        metadata_menu = tools_menu.addMenu("Metadata")

        experiment_menu = tools_menu.addMenu("Experiment setup")

        MI_action = QAction("Motion Imagery Settings",self)
        ##MI_action.triggered.connect(self.open_MI_setting_window)
        
        experiment_menu.addAction(MI_action)

        view_menu = menu.addMenu("View")
        ### view_menu.addAction()

        """
        WIDGETS: main window commands
        """
        # buttons that select the steps of setting up the experiment
        self.button1 = QPushButton("Select stream")
        self.button1.clicked.connect(self.show_stream_selection)

        self.button2 = QPushButton("Select experiment")
        self.button2.clicked.connect(self.show_experiment_setup_window)

        self.button3 = QPushButton("View visual representation\n(don't do this for now)")
        
        self.button4 = QPushButton("View metadata and approve experiment")
        
        self.central_label = QLabel("Info displayed here")
        self.right_label = QLabel("metadata info displayed here")
        self.update_info = QPushButton("Update metadata info") # NOTE: this should be done automatically. perhaps with a function that takes all metadata and puts it together?
        self.update_info.clicked.connect(self.update_metadata)
        self.update_metadata()

        """
        LAYOUT: main window commands
            ...
        """

        self.layout00 = QHBoxLayout() # holds: side bar, central widget for setting/selection, left widget that shows info
        self.layout00.setSpacing(5)

        self.layout01 = QVBoxLayout() # holds buttons on side bar on left
        self.layout00.setSpacing(5)

        self.layout02 = QVBoxLayout() # holds metadata label and update button
        self.layout02.setSpacing(5)
        
        self.layout02.addWidget(self.right_label)
        
        self.update_metadata_button = QPushButton("Update metadata")
        self.update_metadata_button.clicked.connect(self.update_metadata)
        self.layout02.addWidget(self.update_metadata_button)


        self.layout01.addWidget(self.button1)   
        self.layout01.addWidget(self.button2)
        # self.layout01.addWidget(self.button3) not yet time to implement button 3
        self.layout01.addWidget(self.button4)

        self.layout00.addLayout(self.layout01)

        self.layout00.addWidget(self.central_label)
        self.layout00.addLayout(self.layout02)

        dummy = QWidget()
        dummy.setLayout(self.layout00)
        self.setCentralWidget(dummy)


    def exit_action_called(self):
        self.exit()

    def show_stream_selection(self):
        if self.stream_selection.isVisible():
            pass
        else:
            self.stream_selection.show()
            ## self.layout00.removeWidget(self.right_label) IF YOU WANNA KEET THIS IN THE CENTRAL IDGET, FIND A WAY OF CHANGING IT!

    def set_stream(self):
        """
        when the stream selection window accepts the stream, update the input streamInfo object
        NOTE: when working with multiple streams, modify this!
        NOTE: this might be modified later, so metadata gets screwed up!
        """
        if len(self.stream_selection.streams) > 0:
            print(type(self.stream_selection.streams[self.stream_selection.index]))

            if type(self.stream_selection.streams[self.stream_selection.index]) == StreamInfo:

                self.stream_info = self.stream_selection.streams[self.stream_selection.index]
                print("selecting stream ",self.stream_selection.index)
        else:
            print("no labstreaming layer outlet found!")

        self.update_metadata() # update metadata

    def close_stream_selection_window(self):
        self.stream_selection.close()

    def show_experiment_setup_window(self):
        if self.experiment_setup_window.isVisible():
            pass
        else:
            self.experiment_setup_window.show()

    def set_experiment_type(self):
        # updates metadata on experiment type
        text = self.experiment_setup_window.page_combo.currentText()
        self.experiment_info["Experiment Type"] = text # update main window metadata
        print(f"setting {text} as Experiment Type")
        
        # if motion imagery was selected
        if self.experiment_info["Experiment Type"] == "Motion Imagery":
            
            # stimulus duration
            text = self.experiment_setup_window.stimulus_duration.text()
            self.experiment_info["Stimulus Duration"] =  text 
            
            print("Updating motion imagery metadata")
            print("\tstimulus duration:\t" + text) 
            
            #rest time
            text = self.experiment_setup_window.rest_time.text()
            self.experiment_info["Rest Time"] = text # self.experiment_setup_window.page1Layout.
            
            print("\trest time:\t\t" + text) 

            # runs per class
            text = self.experiment_setup_window.runs_per_class.text()
            self.experiment_info["Runs per class"] = text # self.experiment_setup_window.page1Layout.
            
            print("\tRuns per class:\t\t" + text) 


        self.update_metadata() # instead of using the update button
        

    def update_metadata(self):

        text = "Streaming info\n"
        if type(self.stream_info) == StreamInfo:
            text = text + "\tOutlet name\t{}\n\ttype:\t\t{}\n\tchannels\t\t{}\n\tsrate\t\t{}\n\tformat\t\t{}\n\tsource id\t{}".format(self.stream_info.name() , self.stream_info.type() , self.stream_info.channel_count(), self.stream_info.nominal_srate(), self.stream_info.channel_format(), self.stream_info.source_id())
        else: 
            text = text + "\tNo outlet selected"

        # add patient info into self.stream_info.desc() child!
        ...

        # add experiment parameters
        text = text + "\n\nExperiment Type\n\t" + self.experiment_info["Experiment Type"]
        
        # parameter of experiment
        if self.experiment_info["Experiment Type"] == "Motion Imagery":
            text = text + "\nExperiment Parameters\n\tStimulus Duration\t\t{}\n\tRest Time:\t\t{}\n\tRuns per Class\t\t{}".format( self.experiment_setup_window.stimulus_duration.text(), self.experiment_setup_window.rest_time.text(), self.experiment_setup_window.runs_per_class.text() )


        text
        self.right_label.setText(text)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())










