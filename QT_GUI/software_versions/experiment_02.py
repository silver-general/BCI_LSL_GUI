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
                                QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QDialog,
                                QToolBar, QStatusBar,
                                QLabel, QPushButton, QListWidget, QTreeWidget, QComboBox
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
class ExperimentTypeSetupWindow(QWidget):
    """
    open this with self.show_experiment_setup_window() method
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Experiment Type Setup")

        self.layout = QVBoxLayout()

        self.experiment_type = QComboBox()
        self.experiment_type.addItems(["Motion Imagery","SSVEP (not yet vailable)"])
        self.experiment_type.currentIndexChanged.connect(self.selection_changed)

        self.experiment_type = QComboBox()
        self.experiment_type.addItems(["No Experiment Selected","Motion Imagery","SSVEP"])
        self.experiment_type.currentIndexChanged.connect(self.selection_changed)

        self.accept_selection = QPushButton("Accept Selection")
        self.close_window = QPushButton("Close")
        self.close_window.clicked.connect(self.close)

        self.layout.addWidget(QLabel("Selet experiment type"))
        self.layout.addWidget(self.experiment_type)
        self.layout.addWidget(self.accept_selection)
        self.layout.addWidget(self.close_window)

        self.setLayout(self.layout)

    def selection_changed(self):
        print("Experiment selection changed: ")
        print(self.experiment_type.currentIndex())
        print(self.experiment_type.currentText())


class ExperimentParametersSetupWindow(QWidget):
    def __init__(self):
        """
        parameters
            stimuli: choose a number of images or sounds
            stimulus duration
            rest duration
            number of runs
        on the left, a label with a small recap! 
        """
        super().__init__()
        self.setWindowTitle("Experiment Parameters Setup")

        self.experiment_type = "No experiment selected"
        self.info = {} # contains a recap of the selection

        self.layout00 = QHBoxLayout()
        self.layout00.addWidget(QLabel("PARAMETER SETTINGS HERE"))
        self.layout00.addWidget(QLabel("RECAP INFORMATION HERE"))
        self.setLayout(self.layout00)

        self.update_layout()


    def update_layout(self):
            """
            depending on experiment type, you have a different form to fill. in this case, a different self.layout01
            NOTE: this creates a new layout and applies it. is it a good practice? QUESTION
            QUESTION: SOMETHING'S WRONG. I CANNOT DO THIS PARALLEL LAYOUT THING, SHOULD I DELETE SOME? 
                REAAD: https://www.pythonfixing.com/2022/01/fixed-clear-all-widgets-in-layout-in.html
            """
            print("Updating layout for " + self.experiment_type)

            #delete all layouts HOW QUESTION
            """
            for i in reversed(range(self.layout00.count())): 
                self.layout00.itemAt(i).widget().setParent(None)
            """

            if self.experiment_type == "No Experiment Selected":
                pass

            if self.experiment_type == "Motion Imagery":
                
                self.layout00 = QHBoxLayout() # container layout

                self.layout01 = QVBoxLayout()

                """ these buttons are contained in the init so they always exist! of better keep them here? QUESTION"""
                self.label1 = QLabel("Parameters for experiment: Motion Imagery")
                self.tmp1 = QPushButton("MI dummy 1")
                self.tmp2 = QPushButton("MI dummy 2")                

                self.layout01.addWidget(self.label1)
                self.layout01.addWidget(self.tmp1)
                self.layout01.addWidget(self.tmp2)

                self.layout00.addLayout(self.layout01) ##
                self.layout00.addWidget(QLabel("RECAP INFO HERE")) # use self.info dictionary to draw info
                self.setLayout(self.layout00)

            if self.experiment_type == "SSVEP":

                self.layout00 = QHBoxLayout() # container layout

                self.layout02 = QVBoxLayout()

                self.label2 = QLabel("Parameters for experiment: " + self.experiment_type)
                self.tmp3 = QPushButton("dummy 3")
                self.tmp4 = QPushButton("dummy 4")

                self.layout02.addWidget(self.label2)
                self.layout02.addWidget(self.tmp3)
                self.layout02.addWidget(self.tmp4)

                self.layout00.addLayout(self.layout02)

                # recap label and set layout
                self.layout00.addWidget(QLabel("RECAP HERE"))
                self.layout00.addLayout(self.layout02) ##
                self.setLayout(self.layout00)
                


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

        self.experiment_setup_window = ExperimentTypeSetupWindow()
        self.experiment_setup_window.accept_selection.clicked.connect(self.set_experiment_type)

        self.experiment_parameters_setup_window = ExperimentParametersSetupWindow()



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

        self.experiment_parameters_button = QPushButton("Select Experiment parameters")
        self.experiment_parameters_button.clicked.connect(self.show_experiment_parameters_setup_window)

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
        self.layout01.addWidget(self.experiment_parameters_button)
        self.layout01.addWidget(self.button3)
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
        text = self.experiment_setup_window.experiment_type.currentText()
        self.experiment_info["Experiment Type"] = text
        print(f"setting {text} as Experiment Type")
        
        self.update_metadata()# instead of using the update button
        
        self.experiment_parameters_setup_window.experiment_type = text # this sends the info to the window that will do the parameters setup
        self.experiment_parameters_setup_window.update_layout() # this will update they layout according to the requested experiment type
    
    def update_metadata(self):
        text = "Streaming info\n"
        # show stream information
        if type(self.stream_info) == StreamInfo:
            text = text + "\tOutlet name\t\t{}\n\ttype:\t\t{}\n\tchannels\t\t{}\n\tsrate\t\t{}\n\tformat\t\t{}\n\tsource id\t{}".format(self.stream_info.name() , self.stream_info.type() , self.stream_info.channel_count(), self.stream_info.nominal_srate(), self.stream_info.channel_format(), self.stream_info.source_id())
        else: 
            text = text + "\tNo outlet selected"

        # add patient info into self.stream_info.desc() child!
        ...

        # add experiment parameters
        text = text + "\n\nExperiment Type\n\t" + self.experiment_info["Experiment Type"]
        
        text
        self.right_label.setText(text)

    def show_experiment_parameters_setup_window(self):
        if self.experiment_parameters_setup_window.isVisible():
            pass
        else:
            self.experiment_parameters_setup_window.show()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())










