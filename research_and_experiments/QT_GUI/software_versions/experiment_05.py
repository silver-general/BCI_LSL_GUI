import sys
import os 
import numpy as np

from pylsl import StreamInlet, resolve_stream, local_clock, StreamInfo

from PySide6.QtCore import QStandardPaths, Qt, QSize

from PySide6.QtGui import QAction, QIcon

from PySide6.QtWidgets import (
                                QApplication, QMainWindow, 
                                QHBoxLayout, QVBoxLayout, QStackedLayout, QFormLayout, QGridLayout, 
                                QWidget, QDialog, QFileDialog,
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

        
        self.layout.addWidget(self.stream_list)
        self.layout.addWidget(self.update)
        self.layout.addWidget(self.accept)

        self.setLayout(self.layout)

    def update_index(self):

        self.index = self.stream_list.currentRow()
        print("selection changed: ", self.index)

    def scan_streams(self):
        streams = resolve_stream()
        print("looking for streams.")
        self.print_streams_info(streams)

        self.streams = streams

        # add stream info names to list
        self.stream_list.clear()

        if len(streams) > 0:
            for outlet in streams:
                metadata = "outlet name:\t\t{}\n\ttype:\t\t{}\n\tchannels\t\t{}\n\tsrate\t\t{}\n\tformat\t\t{}\n\tsource id\t\t{}".format(outlet.name() , outlet.type() , outlet.channel_count(), outlet.nominal_srate(), outlet.channel_format(), outlet.source_id())
                self.stream_list.addItem(metadata) # self.stream_list is a list of strings! NOT StreamInfo
        else:
            self.stream_list.clear()
            self.stream_list.addItem("No stream found. please update")


        print("streams found: ")
        print(self.streams)

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


class StimulusWidget(QWidget):

    def __init__(self, widget_number):
        super().__init__()

        # store name of selected stimulus
        self.description = {"picture path" : "", "audio path" : ""} # QUESTION: better to use a dictionary here TODO: use only this
        self.picture_path = ""
        self.audio_path = ""
        self.audio_cue_path = ""
        self.stimulus_duration = None # NOTE: should I implement different times for each stimulus? later in the future

        # data path for finding stimuli
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'example_data'))
        print("setting path for stimuli data: ", self.data_path)


        """
        LAYOUT
            each widget is a row that starts as a simple button "add stimulus"
            when the button is pressed, it becomed a row of widgets with
                delete widget button
                file name label
                open picture file button (open the file dialog)
                audio name label
                open audio file button (open the file dialog) 
                    NOTE: if you want to use an auditory stimulus, use this field as well

        """

        self.widget_number = widget_number

        self.picture_label = QLabel("Stimulus Image:")
        self.picture_name = QLabel("...")
        self.browse_image_button = QPushButton("Upload Image")
        self.browse_image_button.clicked.connect(self.browse_image_button_clicked)
        
        self.audio_label = QLabel("Stimulus Audio:")
        self.audio_name = QLabel("...")
        self.browse_audio_button = QPushButton("Upload Audio")
        self.browse_audio_button.clicked.connect(self.browse_audio_button_clicked)

        self.audio_cue_label = QLabel("Audio cue before this stimulus")
        self.audio_cue_name = QLabel("...")
        self.browse_audio_cue_button = QPushButton("Upload Audio Cue")
        self.browse_audio_cue_button.clicked.connect(self.browse_audio_cue_button_clicked)

        self.clear_button = QPushButton("Clear stimulus {} data".format(self.widget_number))
        self.clear_button.clicked.connect( self.clear_stimulus_data )


        """ 
        using a GRID LAYOUT 
        """
        
        self.grid = QGridLayout()

        self.grid.addWidget( QLabel("Stimulus {}".format(widget_number)), 0, 0 )
        self.grid.addWidget( self.picture_label, 1,2 )
        self.grid.addWidget( self.picture_name, 1,3 )
        self.grid.addWidget( self.browse_image_button, 1,4)

        self.grid.addWidget( self.audio_label, 2,2 )
        self.grid.addWidget( self.audio_name, 2,3 )
        self.grid.addWidget( self.browse_audio_button, 2,4 )

        self.grid.addWidget( self.audio_cue_label, 3,2 )
        self.grid.addWidget( self.audio_cue_name, 3,3 )
        self.grid.addWidget( self.browse_audio_cue_button, 3,4 )

        self.grid.addWidget( self.clear_button, 4,4 )

        self.setLayout(self.grid)


    def browse_image_button_clicked(self):
        print("opening browse stimulus dialog")
        ###file_dialog = QFileDialog(self)
        # NOTE: the function returns a tuple, and the first element is the chosen path! second is the filters used. QUESTION why do this?
        file_name = QFileDialog.getOpenFileName(parent = self, caption = "Browse Audio", dir = self.data_path, filter = "")[0]   
            #QUESTION: I cannot make the filter work! I need also audio!

        if len(file_name[0])>0:
            self.picture_path = file_name
            self.description["picture path"] = file_name
            print("a file was selected: ", self.picture_path)
            self.picture_name.setText( file_name.split("/")[-1] ) # updates the label
            
        else:
            print("No file was selected")

    def browse_audio_button_clicked(self):
        print("opening browse stimulus dialog")
        ###file_dialog = QFileDialog(self)
        # NOTE: the function returns a tuple, and the first element is the chosen path! second is the filters used. QUESTION why do this?
        file_name = QFileDialog.getOpenFileName(parent = self, caption = "Browse Image", dir = self.data_path, filter = "")[0]   
            #QUESTION: I cannot make the filter work! I need also audio!

        if len(file_name[0])>0:
            self.audio_path = file_name
            self.description["audio path"] = file_name
            print("a file was selected: ", self.audio_path)
            self.audio_name.setText( file_name.split("/")[-1] ) # updates the label
            
        else:
            print("No file was selected")

    def browse_audio_cue_button_clicked(self):
        
        print("opening browse audio cue dialog")
        ###file_dialog = QFileDialog(self)
        # NOTE: the function returns a tuple, and the first element is the chosen path! second is the filters used. QUESTION why do this?
        file_name = QFileDialog.getOpenFileName(parent = self, caption = "Browse Audio Cue Dialog", dir = self.data_path, filter = "")[0]   
            #QUESTION: I cannot make the filter work! I need also audio!

        if len(file_name[0])>0:
            self.audio_cue_path = file_name
            self.description["audio cue path"] = file_name
            print("a audio cue file was selected: ", self.audio_cue_path)
            self.audio_cue_name.setText( file_name.split("/")[-1] ) # updates the label
            
        else:
            print("No file was selected")

    def clear_stimulus_data(self):
        print("clearing stimulus {} data".format(self.widget_number))
        self.picture_name.setText("...")
        self.audio_name.setText("...")
        self.audio_cue_name.setText("...")

class ExperimentSetupWindow(QWidget):
    """
    open this with self.show_experiment_setup_window() method


    stimulas selection layout
        select stimulus ___ : filename of stimulus : button (remove stimulus)
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Experiment Type Setup")
        
        ########self.experiment_type = "No experiment selected"
        
        self.SSVEP_parameters = {} # NOTE: not yet implemented!

        self.accept_experiment_settings_button = QPushButton("Accept Experiment Settings")
            # signal for this goes into the widget that calls this widget self.accept_experiment_settings_button.clicked.connect(self.accept_experiment_settings)

        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create and connect the combo box to switch between pages
        self.page_combo = QComboBox()
        self.page_combo.addItems(["No Experiment Selected", "Motion Imagery", "SSVEP (not yet vailable)"])

        self.page_combo.activated.connect(self.switchPage)

        # Create the stacked layout
        self.stackedLayout = QStackedLayout()


        """FIRST PAGE  in the case of no selection""" # QUESTION: make this into a custom QWidget so you can edit it outside the main window and just call it. simpler code!
        
        self.page0 = QLabel("Select Experiment type first")

        self.stackedLayout.addWidget(self.page0)


        """SECOND PAGE: MOTION IMAGERY"""
        self.page1 = QWidget()
        self.page1_layout = QVBoxLayout() # external layout

        self.MI_form_layout = QFormLayout()

        # for practice, create a list of widgets to use in the form layout QUESTION: is there a way of putting this in an iterable element?
        self.stimulus_duration = QLineEdit("0")
        self.rest_time = QLineEdit("0")
        self.runs_per_class = QLineEdit("0") # number of runs for each image

        self.settings_form_elements = { "Stimulus duration" : self.stimulus_duration, "Rest time" : self.rest_time, "Number of runs per stimulus" : self.runs_per_class } # NOTE: items are widgets!

        for key in self.settings_form_elements.keys():
            self.MI_form_layout.addRow( key, self.settings_form_elements[key] )


        # motion imagery stimuli: you must be able to add, remove
        self.stimuli_layout = QVBoxLayout()
        
        # add custom widgets for browsing stimuli data, as a list
        self.stimuli_list = [ StimulusWidget(widget_number = 0), StimulusWidget(widget_number = 1), StimulusWidget(widget_number = 2), StimulusWidget(widget_number = 3)]

        for i in self.stimuli_list:
            self.stimuli_layout.addWidget(i)

        self.generate_MI_button = QPushButton("Generate MI sequence")
        self.generate_MI_button.clicked.connect(self.generate_MI_sequence)


        self.page1_layout.addLayout(self.MI_form_layout)
        # delete this self.page1_layout.addWidget(self.audio_cue_browse_button )
        self.page1_layout.addLayout(self.stimuli_layout)
        self.page1_layout.addWidget(self.generate_MI_button)

        self.page1.setLayout(self.page1_layout)

        self.stackedLayout.addWidget(self.page1)


        """THIRD PAGE SSVEP (not yet implemented)"""
        self.page2 = QWidget()
        self.page2_layout = QFormLayout()
        self.page2_layout.addRow("Parameter 1", QLineEdit())
        self.page2_layout.addRow("Parameter 2", QLineEdit())

        self.page2.setLayout(self.page2_layout)

        self.stackedLayout.addWidget(self.page2)


        """Add the combo box and the stacked layout to the top-level layout"""
        layout.addWidget(self.page_combo)
        layout.addLayout(self.stackedLayout)
        layout.addWidget(self.accept_experiment_settings_button)

    def switchPage(self):
        """
        switches page AND updates experiment type! 
        """
        self.stackedLayout.setCurrentIndex(self.page_combo.currentIndex())
        
        text = self.page_combo.currentText()
        print("switching to experiment type: ", text)
        self.experiment_type = text

    def selection_changed(self):
        print("Experiment selection changed: ")
        print(self.experiment_type.currentIndex())
        print(self.experiment_type.currentText())

    def restore_defaults(self):
        """QUESTION ONE DAY DO THIS"""
        pass

    def generate_MI_sequence(self):
        """
        generates a series of motor imagery stimuli plus resting time plus audio cues
        parameters to use
            stimuli
                the number of classes to show. basic case, it's 2
            stimulus duration
                time that a stimulus is displayed
            runs per stimuli
                each stimulus will be run "n" times
            rest stimulus
                during resting time, show something
            rest duration
                how long does the resting last
            audio cue
                ...
        EXAMPLE
            - 2 classes, duration in 5s, 20 times each stimulus, 1 rest image, rest time is 10s, 
            - create a list of 40 images, shuffle, then add rest image in the middle
            - if a stimulus is a sound, use a default black screen

        HOW
            experiment settings are kept in the MainWindow experiment_settings dictionary

        """
        
        """ 1) GENERATING A SEQUENCE OF INDEXES """
        print("GENERATING SEQUENCE")
        # step 1: create a list of N elements
            # there are k classes, k: number of stimuli
            # each class repeats n times, n : runs per class
            # N = k*n
        k = len(self.stimuli_list) # already defined above. rewrite it someday
        n = int(self.runs_per_class.text())
        N = k*n
        sequence = np.zeros(0)
        for i in range(k):
            sequence = np.append( sequence, np.ones(n)*i )

        """ print some information on terminal """
        print("number of classes: ", k)  
        print("Experiment settings:") 
        for key in self.settings_form_elements.keys():
            print("\t",key,"\t",self.settings_form_elements[key].text())
        
        for stimulus in self.stimuli_list:
            print("Stimulus ",stimulus.widget_number)
            print("\tpicture\t",stimulus.picture_path)
            print("\taudio\t",stimulus.audio_path)

        print("GENERATED SEQUENCE:")
        print(sequence)

        """ 2) CREATING A PLAYLIST
        all elements have the same duration
        some elements have audio. I will need to add audio 
        """


class PatientDataWindow(QWidget):
    """
    editable labels with possibility of adding more info about a patient through an "add" and "remove" buttons
    """        
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Patient Data Setting")
        
        self.layout = QVBoxLayout()

        self.accept_settings = QPushButton("Accept settings")

        self.name = QLineEdit("") # QUESTION: HOW TO I CREATE AN INTERACTIVE "insert new form" ??
        self.surname = QLineEdit("") 
        self.birthday = QLineEdit("") 
        ##self.EEG_technician = QLineEdit("") NOTE: NOT A PATIENT THING!

        self.patient_data_entries = { "Name" : self.name, "Surname" : self.surname, "Birthday" : self.birthday }

        self.patient_data_form = QFormLayout()

        for key in self.patient_data_entries.keys():
            self.patient_data_form.addRow(key, self.patient_data_entries[key])
        
        self.layout.addLayout(self.patient_data_form)

        self.layout.addWidget(self.accept_settings)

        self.setLayout(self.layout)
    
    def add_row_to_form(self):
        """
        adds another row
        """
        ...


class ApproveExperimentWindow(QWidget):
    """
    open this with self.show_approve_experiment_window() method
    QUESTION: this is only for motion imagery. later find a way of differentiating for SSVEP and others!
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Approve Experiment Window")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.metadata_label = QLabel("StreamInfo complete with all metadata (can I generate timestamps already? or get a button to do so?") 
            # NOTE: text is set when main window updates the etadata. is that okay? I'll append things to the StreamInfo object there. QUESTION
        
        self.approve_and_run_button = QPushButton("Approve and Run")


        self.layout.addWidget(self.metadata_label)
        self.layout.addWidget(self.approve_and_run_button)


class DummyWidget(QWidget):
        def __init__(self):
            super().__init__()
            label = QLabel("dummy label")
            layout= QHBoxLayout()
            layout.addWidget(label)
            self.setLayout(layout)



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("A LSL-based GUI")


        """ 
        structures to store metadata
            NOTE: data can also be stored into the widgets contained in the MainWindow. BUT if I do this, then I can change the widgets without having to change the mainwindows methods! """

        self.stream_info = StreamInfo() # list of available StreamInfo objects holding metadata for LSL stream outlets

        self.patient_data = {"Name": "No Name", "Surname":"No Surname","Birthday":"No Date"} # this will hold the outlet metadata as well as additional features like the motor imagery timing and patient data
        self.patient_data_default = {"Name": "No Name", "Surname":"No Surname","Birthday":"No Date"}
        
        self.experiment_info = {"Experiment Type" : "No experiment selected"}
        self.experiment_info_default = {"Experiment Type" : "No experiment selected"}


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

        MI_action = QAction("Motion Imagery Settings",self) # this is not used! remove and remove the menu item that references this!
        ##MI_action.triggered.connect(self.open_MI_setting_window)
        experiment_menu.addAction(MI_action)

        view_menu = menu.addMenu("View")


        """
        BUTTONS FOR LAYOUT 2
        """
        self.stream_selection_button = QPushButton("Select stream")
        self.stream_selection_button.clicked.connect(self.show_stream_selection_window)

        self.experiment_selection_button = QPushButton("Select experiment")
        self.experiment_selection_button.clicked.connect(self.show_experiment_setup_window)

        #### NOTE NOT YET AVAILABLE: ASK CIHAN FOR MORE INFO
        ### self.button3 = QPushButton("View visual representation\n(don't do this for now)")
        
        self.patient_data_button = QPushButton("Insert Patient Data")
        self.patient_data_button.clicked.connect(self.show_patient_data_window)

        self.view_metadata_and_run_experiment_button = QPushButton("View metadata and approve experiment")
        self.view_metadata_and_run_experiment_button.clicked.connect(self.show_approve_experiment_window)
        

        """
        LAYOUT 
            ...
        """
        self.central_layout = QHBoxLayout()


        """LEFT COLUMN OF BUTTONS"""

        self.left_column_buttons_layout = QVBoxLayout()
        self.left_column_buttons_layout.addWidget(self.stream_selection_button)
        self.left_column_buttons_layout.addWidget(self.experiment_selection_button)
        self.left_column_buttons_layout.addWidget(self.patient_data_button)
        self.left_column_buttons_layout.addWidget(self.view_metadata_and_run_experiment_button)

        self.central_layout.addLayout(self.left_column_buttons_layout)


        """STACKED LAYOUT: DIFFERENT PAGES FOR SETTINGS"""

        self.settings_layout = QStackedLayout()

        self.settings_layout_index = 0 # use this to change page when pressing buttons


        # PAGE 1: STREAM SELECTION
        self.page1 = StreamSelectionWindow()
        self.page1.accept.clicked.connect(self.set_stream)
        self.settings_layout.addWidget(self.page1)

        # PAGE 2: ...
        self.page2 = ExperimentSetupWindow()
        self.page2.accept_experiment_settings_button.clicked.connect(self.accept_experiment_settings)
        self.settings_layout.addWidget(self.page2)

        # PAGE 3
        self.page3 = PatientDataWindow()
        self.page3.accept_settings.clicked.connect(self.accept_patient_data)
        self.settings_layout.addWidget(self.page3)
        
        # PAGE 4
        self.page4 = ApproveExperimentWindow()
        self.page4.approve_and_run_button.clicked.connect(self.approve_and_run_experiment)
        self.settings_layout.addWidget(self.page4)

        self.central_layout.addLayout(self.settings_layout)
        

        """LEFT LABEL WITH METADATA"""
        self.metadata_label = QLabel("METADATA updated here")
        #self.metadata_label.setFixedWidth(200) QUESTION: HOW TO get a decent thing here?
        self.central_layout.addWidget(self.metadata_label)


        """ASSIGN CENTRAL WIDGETS"""
        dummy = QWidget()
        dummy.setLayout(self.central_layout)

        self.setCentralWidget(dummy)


    def exit_action_called(self):
        self.exit()

    def switch_page(self):

        self.settings_layout.setCurrentIndex(self.settings_layout_index)


    def show_stream_selection_window(self):
        
        self.settings_layout_index = 0
        print("switching settings staked layout to page : ",self.settings_layout_index)
        self.switch_page()

    def set_stream(self):
        """
        when the stream selection window accepts the stream, update the input streamInfo object
        NOTE: when working with multiple streams, modify this!
        """

        print("SETTING STREAM...")


        if len( self.page1.streams ) > 0:

            if type(self.page1.streams[ self.page1.index ]) == StreamInfo:
                self.stream_info = self.page1.streams[self.page1.index]
                print("selecting stream ",self.stream_info.name())
        else:
            print("\tno labstreaming layer outlet found!")
            # QUESTION: need a way of telling the user that no streaming was found. use a dialog!

        self.update_metadata() # update metadata


    def show_experiment_setup_window(self):

        self.settings_layout_index = 1
        print("switching settings staked layout to page : ",self.settings_layout_index)
        self.switch_page()

    def accept_experiment_settings(self):
        # update experiment type
        text = self.page2.experiment_type
        print("\nAPPROVING EXPERIMENT SETTINGS:")
        print("\tExperiment type\n\t\t",text)
        self.experiment_info[ "Experiment Type" ] = text

        if self.page2.experiment_type == "Motion Imagery":

            # setup MI parameters in the main window self.experiment_info dictionary using the ExperimentSetupWindow (experiment_setup_window.MI_form_layout)
            # QUESTION: find a way of automating this, for example keeping a list of 
            print("\tParameters")
            for key in self.page2.settings_form_elements.keys():
                text = self.page2.settings_form_elements[key].text()
                print("\t\t",key,"\t",text) 
                self.experiment_info[key] = text       # NOTE: values are QLine edit
        

            # ADD STIMULI TO A LIST in MainWindow
            # self.page2 is the ExperimentSetupWindow widget
                # self.page2.stimuli_list is a list where the programmer has manually added some widgets
                    # each of the stimuli contains a path to an image or an audio or both! they are called .picture_path and .audio_path
            for stimulus_widget in self.page2.stimuli_list: # i is a widget! get its .stimulus attribute, that holds the path!

                print("\tAdding stimulus: ",stimulus_widget.widget_number)
                print(stimulus_widget.description)

                # addi stimulus to experiment info dictionary in MainWindow
                self.experiment_info[ "stimulus {}".format(stimulus_widget.widget_number) ] = stimulus_widget.description 

        # update metadata label
        self.update_metadata() # TODO: update this function, as you changed the stimulus widget!



    def show_patient_data_window(self):
        self.settings_layout_index = 2
        print("switching settings staked layout to page : ", self.settings_layout_index)
        self.switch_page()

    def accept_patient_data(self):
        """
        here you accept sna dsave to metadata all patient settings found in the form
        metadata in main window self.patient_data dictionary is updated using the dictionary "self.patient_data_entries" in the PatientDataWindow widget
        """
        print("\nACCEPTING PATIENT DATA")
        for key in self.page3.patient_data_entries.keys():
            
            print( "\t{}\t\t{}".format( key, self.page3.patient_data_entries[key].text() ) )

            self.patient_data[key] = self.page3.patient_data_entries[key].text() # QUESTION: NOW THAT i THINK OF IT, THIS IS A MEANINGLESS STEP. DATA IS ALREADY STORED SOMEWHERE, I'M JUST COPYING IT IN THE MAIN WINDOW ATTRIBUTE!

        self.update_metadata()
        
 
    def show_approve_experiment_window(self):
        self.settings_layout_index = 3
        print("switching settings staked layout to page : ", self.settings_layout_index)
        self.switch_page()

    
        

    def approve_and_run_experiment(self):
        """
        remember to take the infos from the respective dictionaries and assemble the metadata by appending children
        metadata stored in
            self.stream_info, StreamInfo object
            self.patient_data, dictionary
            self.experiment_info, dictionary
        how:
            info.desc().append_child("Patient Data")
        """
        print("EXPERIMENT APPROVED! NOW RUNNING!")
        
        # assemble metadata together into one big XML file (append to the StreamInfo selected)
        info = self.stream_info

        patient_data = info.desc().append_child("Patient Data")
        for key in self.patient_data.keys():
            patient_data.append_child_value(key,self.patient_data[key])

        experiment_info = info.desc().append_child("Experiment Info")
        for key in self.experiment_info.keys():
            experiment_info.append_child_value( key, self.experiment_info[key] )

        print(info.as_xml())

        """
        AND NOW, RUN THE EXPERIMENT. HOW? NEW WIDGET? SHOULD I USE A DIALOG? SO THAT THERE'S NO COMPUTATION FOR THE OTHER WIDGETS!
        """
            

    def update_metadata(self):
        """
        this will update the label (self.metadata_label) by running through the metadata dictionaries. 
        final metadata will be appended to the StreamInfo object when finally approving the experiment
        """

        print("UPDATING METADATA LABEL")

        text = ""

        # take info out of the StreamInfo object, if any
        if type(self.stream_info) == StreamInfo:
            text = text + "Streaming Info\n\tOutlet name\t{}\n\ttype:\t\t{}\n\tchannels\t\t{}\n\tsrate\t\t{}\n\tformat\t\t{}\n\tsource id\t{}".format(self.stream_info.name() , self.stream_info.type() , self.stream_info.channel_count(), self.stream_info.nominal_srate(), self.stream_info.channel_format(), self.stream_info.source_id())
        else: 
            text = text + "Streaming Info\n\tNo outlet selected"
        
        # take experiment info from self.experiment_info, a dictionary
        text = text + "\nExperiment Info\n"
        for key in self.experiment_info.keys():

            if type(self.experiment_info[key]) == dict: # if dictionary, it means it's the stimulus dictionary. unpack it
                
                text = text + "\t{}\n".format(key)
                
                for inner_key in self.experiment_info[key].keys():
                    text = text + "\t\t{}\t\t{}\n".format(inner_key, self.experiment_info[key][inner_key].split("/")[-1] ) # QUESTION: how to shrink the widget? for now I only use the filename

            else:
                text = text + "\t{}\t\t{}\n".format(key,self.experiment_info[key])
        
        print("\tExperiment Info", self.experiment_info)


        # take patient data info from patient_data, it's a dictionary
        text = text + "Patient Data\n"
        for key in self.patient_data.keys():
            text = text + "\t{}\t\t{}\n".format(key, self.patient_data[key])

        print("\tPatient data: ", self.patient_data)

        #text = text + "\nPatient data\n\tname\t\t{}\n\tsurname\t{}\n\tDate of Birth\t{}".format( self.patient_data["Name"], self.patient_data["Surname"], self.patient_data["Date of Birth"] )

        """
        # take patient daya info from patient_data, it's a dictionary
        text = "Patient Data\n"
        text = text + "\nPatient data\n\tname\t\t{}\n\tsurname\t{}\n\tDate of Birth\t{}".format( self.patient_data["Name"], self.patient_data["Surname"], self.patient_data["Date of Birth"] )
        """
        """
        # take experiment info from self.experiment_info dictionary
        print("Experiment Info:")
        for key in self.experiment_info.keys():
            print("\t{}\t\t{}".format( key, self.experiemnt_info[key] ))
        """

        self.metadata_label.setText(text)

        # IF you want to use the label instead on the streaminfo XML format self.page4.metadata_label.setText( text )


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

