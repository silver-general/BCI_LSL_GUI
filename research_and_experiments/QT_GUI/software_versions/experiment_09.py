import sys
import os 
import numpy as np
import copy

from pylsl import StreamInlet, resolve_stream, local_clock, StreamInfo

from PySide6.QtCore import QStandardPaths, Qt, QSize

from PySide6.QtGui import QAction, QIcon

from PySide6.QtWidgets import (
                                QApplication, QMainWindow, 
                                QHBoxLayout, QVBoxLayout, QStackedLayout, QFormLayout, QGridLayout, 
                                QWidget, QDialog, QFileDialog, QDialogButtonBox, QPlainTextEdit,
                                QToolBar, QStatusBar,
                                QLabel, QLineEdit, QPushButton, QListWidget, QTreeWidget, QComboBox, QListWidget, QTextEdit
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


class Stimulus():
    def __init__(self, stimulus_number):
        #super().__init__()
        self.stimulus_number = stimulus_number
        self.description = {"picture" : "", "audio" : "", "audio_cue" : ""} # TODO add, "stimulus duration" : "0"} 
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'example_data'))
        print("setting path for stimuli data: {}".format(self.data_path))

    # NOTE I cannot access this from the ExperimentSetup window, the opening file dialog complains it receives no arguments! why?


class EditStimulus(QDialog):
    
    def __init__(self, number, stimulus):
        super().__init__()

        # hold the uploaded data into this dictionary, copy it into the widget object when approved
        self.description = stimulus.description # use this to modify paths and print them
        self.number = number
        self.new_description = self.description.copy()

        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'example_data'))

        self.setWindowTitle("Editing stimulus {}".format(self.number))


        # outer layout: contains a list widget, and buttons
        layout = QVBoxLayout()
        self.setLayout(layout)

        # QList widget
        self.info_text = QListWidget()
        self.info_text.currentRowChanged.connect(self.list_row_changed)
        self.info_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.info_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)


        self.update_info_text()
        layout.addWidget(self.info_text)

        # add layout with buttons: add image, add audio, add audio cue, clear all
        button_grid = QGridLayout()

        upload_new = QPushButton("Upload new")
        upload_new.clicked.connect(self.upload_new_item)

        clear_selected = QPushButton("Clear selected")
        clear_selected.clicked.connect(self.clear_selected_item)

        button_grid.addWidget( upload_new, 0,0 )
        button_grid.addWidget( clear_selected, 0,1 )



        # QDialogButtonBox: line of buttons, automatically ordered!
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        # signals: they come from the default buttons you inserted! and you connect the the default accept and reject methods of a QDialog!
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


        layout.addLayout(button_grid)
        layout.addWidget(self.buttonBox)


        """ MOTOR IMAGERY UPLOADING STIMULI FUNCTIONS """
        
    def get_info(self):
        return self.new_description # returns uploaded things

    def list_row_changed(self,row):
        print("list row changed, now on {}".format(row))

    def update_info_text(self):
        # updates a list widget! 
        self.info_text.clear()

        print("updating QList Widget showing stimulus description")
        print("stimulus new description:\t{}".format(self.new_description))

        dict_keys = list(self.new_description.keys()) 

        for i in range ( len( dict_keys ) ):
            # update the QListWidget, row by row, by following the new_description dictionary
            key = dict_keys[i]
            self.info_text.addItem( "{}\t{}".format( key, self.new_description[key].split("/")[-1]  ) )
        
    def upload_new_item(self):
        
        print("Editing stimulus {}".format(self.number))
        
        file_name = QFileDialog.getOpenFileName(parent = self, caption = "Browse", dir = self.data_path, filter = "")[0]   
            
        if len(file_name)>0:
            key = self.info_text.currentItem().text().split(" ")[0].split("\t")[0]
            print("setting new key: {}".format (key) )

            self.new_description[ key ] = file_name  # updates the information corresponding to the seleted row
            print("a file was selected: ", self.new_description[key])
            self.update_info_text()
            
        else:
            print("No file was selected")
    
    def clear_selected_item(self):
        pass


class ExperimentSetupWindow(QWidget):
    """
    open this with self.show_experiment_setup_window() method

    """

    def __init__(self):
        super().__init__()
        
        self.experiment_type = ""

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

        # for practicality, create a list of widgets to use in the form layout 
        self.stimulus_duration = QLineEdit("0")
        self.rest_time = QLineEdit("0")
        self.runs_per_class = QLineEdit("0") # number of runs for each image

        self.settings_form_elements = { "Stimulus duration" : self.stimulus_duration, "Rest time" : self.rest_time, "Number of runs per stimulus" : self.runs_per_class } # NOTE: items are widgets!

        for key in self.settings_form_elements.keys():
            self.MI_form_layout.addRow( key, self.settings_form_elements[key] )


        # stimuli layout:  you must be able to add, remove
        stimuli_layout = QVBoxLayout()

        # list of widgets label
        list_widget_label = QLabel("All stumuli here")

        # keep stimuli into a SCROLLABLE list
        self.list_widget = QListWidget()
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.list_widget.currentRowChanged.connect( self.list_item_changed )
        
        # add custom widgets for browsing stimuli data, as a list
        self.s0 = Stimulus(stimulus_number = 0)
        self.s1 = Stimulus(stimulus_number = 1)
        self.s2 = Stimulus(stimulus_number = 2)
        self.s3 = Stimulus(stimulus_number = 3)
        self.stimuli_list = [ self.s0, self.s1, self.s2, self.s3]

        self.update_list_widget()

        button_grid = QGridLayout()
        edit_b = QPushButton("Edit selected") # edits selected stimulus
        edit_b.clicked.connect(self.edit_stimulus)
        clear_b = QPushButton("Clear Selected") # ...
        add_stim_b = QPushButton("Add stimulus (not available)")
        delete_stim_b = QPushButton("Delete stimulus (not available)")

        button_grid.addWidget(edit_b,0,0)
        button_grid.addWidget(clear_b,0,1)
        button_grid.addWidget(add_stim_b,1,0)
        button_grid.addWidget(delete_stim_b,1,1)


        """
        FIXME QUESTION
        should I use a combobox with "add picture", "add audio", add runup image", "add rest image"?
        let's use a button with "edit stimulus" so you can edit all in a qdialog! or a qwidget.
        
        """



        stimuli_layout.addWidget(list_widget_label)
        stimuli_layout.addWidget( self.list_widget )
        stimuli_layout.addLayout(button_grid)




        self.page1_layout.addLayout(self.MI_form_layout)
        self.page1_layout.addLayout(stimuli_layout)

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

    def list_item_changed(self):
        print("MI stimuli selection changed to stimulus {}".format( self.list_widget.currentRow() ))
        # QUESTION: when clearing a stimulus, the index is set to the last row. why? FIXME!

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
        self.experiment_type = self.page_combo.currentText()

    def restore_defaults(self):
        """QUESTION ONE DAY DO THIS"""
        pass

    def edit_stimulus(self):

        stimulus = self.stimuli_list[self.list_widget.currentRow()]

        dlg = EditStimulus( self.list_widget.currentRow(), stimulus )

        if dlg.exec_():
            print("Setup accepted!")
            print("Previous info: {}".format(stimulus.description))
            print(dlg.get_info()) # NOTE: you can store values and retrieve them when the dialog is not in its loop like this!
            for key in dlg.new_description.keys():
                stimulus.description[key] = dlg.new_description[key]
            print("Updated info: {}".format(stimulus.description))

            self.update_list_widget()

        else: 
            print("Dialog rejected!")

    def update_list_widget(self):
        self.list_widget.clear()
        for stim in self.stimuli_list:
            self.list_widget.addItem( self.unpack( stim ) )

    def unpack(self, stimulus):
        """
        given a StimulusWidget widget, unpacks its info into text that is printed as an element of a QListWidget
        """
        text = "Stimulus {}\n".format(stimulus.stimulus_number)
        
        for key in stimulus.description.keys():
            text = text + "\t{}\t{}\n".format(key,stimulus.description[key].split("/")[-1]) # QUESTION TODO should I return the full path or just the name?

        return text


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

        self.metadata_preview_text = ""

        # layout: depends on selected experiment type
        stacked_layout = QStackedLayout()

        self.setLayout(stacked_layout)

        """FIRST PAGE: NO SELECTION"""
        page0 = QWidget()

        """SECOND PAGE: MI EXPERIMENT"""
        page1 = QWidget()

        page1_layout = QVBoxLayout()

        self.update_metadata_preview_b = QPushButton("Click to generate an XML-formatted metadata")
        self.update_metadata_preview_b.clicked.connect(self.update_metadata_preview)

        self.metadata_preview = QTextEdit("Motor Imagery StreamInfo complete with all metadata (can I generate timestamps already? or get a button to do so?") 
        self.metadata_preview.setReadOnly(True)
        self.metadata_preview.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadata_preview.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadata_preview.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
 

        self.generate_MI_button = QPushButton("Generate MI sequence")

        self.approve_and_run_button = QPushButton("Approve and Run")
        page1_layout.addWidget(self.update_metadata_preview_b)
        page1_layout.addWidget(self.metadata_preview)
        page1_layout.addWidget(self.generate_MI_button)
        page1_layout.addWidget(self.approve_and_run_button)
        page1.setLayout(page1_layout)



        """ THIRD PAGE: SSVEP"""
        page2 = QWidget()


        """ ADD PAGES TO STACKED LAYOUT"""
        stacked_layout.addWidget(page0)
        stacked_layout.addWidget(page1)
        stacked_layout.addWidget(page2)

        # TODO find a way of selecting experiment type. for example, when selecting experiment type in the other widget, send a signal and change it here!
        # for now, put it always on the MI
        stacked_layout.setCurrentIndex(1)

    
    def update_metadata_preview(self):
        print("Updating motor imagery metadata preview")
        self.metadata_preview.clear()
        self.metadata_preview.setText(self.metadata_preview_text)




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
        self.page4.update_metadata_preview_b.clicked.connect(self.create_xml_metadata_preview)
        self.page4.generate_MI_button.clicked.connect(self.generate_MI_sequence)


        self.settings_layout.addWidget(self.page4)

        self.central_layout.addLayout(self.settings_layout)
        

        """RIGHT LABEL WITH METADATA"""
        self.metadata_text = QTextEdit("METADATA updated here")
        self.metadata_text.setReadOnly(True)
        self.metadata_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadata_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadata_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.update_metadata()

        self.central_layout.addWidget(self.metadata_text)


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
            for stimulus in self.page2.stimuli_list: # i is a widget! get its .stimulus attribute, that holds the path!

                print("\tAdding stimulus: ",stimulus.stimulus_number)
                print(stimulus.description)

                # addi stimulus to experiment info dictionary in MainWindow
                self.experiment_info[ "stimulus {}".format(stimulus.stimulus_number) ] = stimulus.description 

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

    def create_xml_metadata_preview(self):
        # assemble metadata together into one big XML file (append to the StreamInfo selected)
        print("creating metadata preview: ")

        info = self.stream_info

        patient_data = info.desc().append_child("Patient Data")
        for key in self.patient_data.keys():
            patient_data.append_child_value(key,self.patient_data[key])

        experiment_info = info.desc().append_child("Experiment Info")

        # TODO something's wrong here
        """
        try to figure out how to extrac info from here
            experiment info: {'Experiment Type': 'Motion Imagery', 'Stimulus duration': '0', 'Rest time': '0', 'Number of runs per stimulus': '0', 
            'stimulus 0': {'picture': '', 'audio': 'C:/Users/alber/Documents/ingegneria/DTU/principles_of_BCI/special_project_2022/code/BCI_LSL_GUI/QT_GUI/example_data/kitten.wav', 'audio_cue': ''}, 
            'stimulus 1': {'picture': '', 'audio': '', 'audio_cue': ''}, 
            'stimulus 2': {'picture': '', 'audio': '', 'audio_cue': ''}, 
            'stimulus 3': {'picture': '', 'audio': '', 'audio_cue': ''}}
        """
        print("appending experiment info to metadata")
        print("experiment info: {}".format(self.experiment_info))
        for key in self.experiment_info.keys():
            if type( self.experiment_info[key] ) is not dict:
                experiment_info.append_child_value( key, self.experiment_info[key] )
            else: # if a dictionary, it's a stimulus data!
                stimulus_info = experiment_info.append_child(key)
                for inner_key in self.experiment_info[key].keys():
                    stimulus_info.append_child_value(inner_key, self.experiment_info[key][inner_key])
        print(info.as_xml())
        
        self.page4.metadata_preview_text = info.as_xml()
        self.page4.update_metadata_preview()
 
    def generate_MI_sequence(self):
        """
        generates a series of motor imagery stimuli plus resting time plus audio cue

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

        stimuli_list = self.page2.stimuli_list
        runs_per_class = self.page2.runs_per_class.text()
        experiment_settings_form = self.page2.settings_form_elements

        k = len(stimuli_list) # already defined above. rewrite it someday
        n = int(runs_per_class)
        N = k*n
        sequence = np.zeros(0)
        for i in range(k):
            sequence = np.append( sequence, np.ones(n)*i )

        """ print some information on terminal """
        print("number of classes: ", k)  
        print("Experiment settings:") 
        for key in experiment_settings_form.keys():
            print("\t",key,"\t",experiment_settings_form[key].text())
        
        for stimulus in stimuli_list:
            for key in stimulus.description.keys():
                print(key,"\t",stimulus.description[key])

        print("GENERATED SEQUENCE:")
        print(sequence)

        """ 2) CREATING A PLAYLIST
        all elements have the same duration
        some elements have audio. I will need to add audio 
        
        """


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
        this will update the label (self.metadata_text) by running through the metadata dictionaries. 
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
                    text = text + "\t\t{}\t\t{}\n".format(inner_key, str(self.experiment_info[key][inner_key]).split("/")[-1] )

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

        self.metadata_text.setText(text)

        # IF you want to use the label instead on the streaminfo XML format self.page4.metadata_text.setText( text )


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())














