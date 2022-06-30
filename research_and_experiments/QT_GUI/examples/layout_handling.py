"""
HOW TO ADD OR REMOVE WIDGETS FROM A LAYOUT
I want to have an add stimulus line which as

add stimulus:
    when clicked, becomes "remove stimulus button" and on the same line
    browse, label with name, stimulus duration
"""

import sys
import os

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                QVBoxLayout, QHBoxLayout, QGridLayout,
                                QPushButton, QLabel, QLineEdit,
                                QDialog, QDialogButtonBox, QFileDialog)


class removeStimulusDialog(QDialog):

    def __init__(self, parent = None):

        super().__init__(parent) 

        self.setWindowTitle("Choose Dialog to Delete!")

        # buttons: mask that tells QT which one to use
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.index = 0

        # QDialogButtonBox: line of buttons, automatically ordered!
        self.buttonBox = QDialogButtonBox(buttons)
        # signals: they come from the default buttons you inserted!
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QHBoxLayout()

        message = QLabel("Select stimulus number and accept:")
        self.line_edit = QLineEdit("")
        self.line_edit.textChanged.connect(self.update_index)

        self.layout.addWidget(message)
        self.layout.addWidget( self.line_edit )
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def update_index(self):
        # question: write a check that this is an integer!
        self.index = int(self.line_edit.text())


class StimulusWidget(QWidget):

    def __init__(self, widget_number):
        super().__init__()

        # store name of selected stimulus
        self.picture_path = ""
        self.audio_path = ""
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

        ######self.grid.addWidget( self.remove_stimulus_button, 3,4 )

        self.setLayout(self.grid)


    def browse_image_button_clicked(self):
        print("opening browse stimulus dialog")
        ###file_dialog = QFileDialog(self)
        # NOTE: the function returns a tuple, and the first element is the chosen path! second is the filters used. QUESTION why do this?
        file_name = QFileDialog.getOpenFileName(parent = self, caption = "Browse Audio", dir = self.data_path, filter = "")[0]   
            #QUESTION: I cannot make the filter work! I need also audio!

        if len(file_name[0])>0:
            self.picture_path = file_name
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
            print("a file was selected: ", self.audio_path)
            self.audio_name.setText( file_name.split("/")[-1] ) # updates the label
            
        else:
            print("No file was selected")



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.stimuli_widgets = []
        self.stimuli_index = 0
        
        self.layout = QVBoxLayout()
 
        button = QPushButton("add stimulus widget")
        button.clicked.connect(self.add_stimulus)
        self.layout.addWidget(button)

        button2 = QPushButton("Remove stimulus widget")
        button2.clicked.connect(self.remove_stimulus)
        self.layout.addWidget(button2)

        dummy = QWidget()
        dummy.setLayout(self.layout)
        self.setCentralWidget(dummy)
    

    def add_stimulus(self):
        
        stimulus = StimulusWidget(self.stimuli_index)
        ###stimulus.remove_stimulus_button.clicked.connect(self.remove_stimulus)

        self.stimuli_index += 1
        self.stimuli_widgets.append( stimulus )

        self.layout.addWidget( stimulus )

    def remove_stimulus(self):
        
        dlg = removeStimulusDialog()
        print("Removing stimulus")
        if dlg.exec_():
            print("Dialog accepted! Deleting stmulus ",dlg.index)
            # QUESTION: how to implement this? I still don't know
        else: 
            print("Dialog rejected!")
    

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()


if __name__=="__main__":
    main()

