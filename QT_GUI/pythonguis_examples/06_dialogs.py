import sys
import os # this only works on windows?
from PySide6.QtWidgets import (QApplication, QMainWindow, 
                                QVBoxLayout,
                                QPushButton, QLabel,
                                QDialog, QFileDialog, QDialogButtonBox)

class CustomDialog(QDialog):
    """
    - the dialog instance can inherit a parent window. remember to pass it!
    - layout buttons: you can use the default buttons from the QButtonDialog namespace
    - You can construct a line of multiple buttons by OR-ing them together using a pipe (|)

    
    - procedure:
        1) create a button mask
            buttons list:
                QDialogButtonBox.Ok
                QDialogButtonBox.Open
                QDialogButtonBox.Save
                QDialogButtonBox.Cancel
                QDialogButtonBox.Close
                QDialogButtonBox.Discard
                QDialogButtonBox.Apply
                QDialogButtonBox.Reset
                QDialogButtonBox.RestoreDefaults
                QDialogButtonBox.Help
                QDialogButtonBox.SaveAll
                QDialogButtonBox.Yes
                QDialogButtonBox.YesToAll
                QDialogButtonBox.No
                QDialogButtonBox.Abort
                QDialogButtonBox.Retry
                QDialogButtonBox.Ignore
                QDialogButtonBox.NoButton
        2) create a button box (a line of buttons) using the mask as parameter
            - EXAMPLE: buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        3) connect signals
            - example 
                self.buttonBox.accepted.connect(self.accept)
                self.buttonBox.rejected.connect(self.reject)
            - NOTE: self.accept and self.reject are the values returned by the dlg.exec_() that calls the dialog loop!
        4) set the button box into the dialog layout
    """
    def __init__(self, parent = None):
        """
        NOTE: super() is initialised with the parent window this is how you tell QT that the QDialog has a parent window!
        """
        super().__init__(parent) 

        self.setWindowTitle("HELLO!")

        # buttons: mask that tells QT which one to use
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        # QDialogButtonBox: line of buttons, automatically ordered!
        self.buttonBox = QDialogButtonBox(buttons)
        # signals: they come from the default buttons you inserted!
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        message = QLabel("Something happened, is that OK?")

        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

# just a tmemporary window
class MainWindow1(QMainWindow):

    def __init__(self):
        super().__init__()


    def closeEvent(self, event):
        self._ensure_stopped()
        event.accept()

    # USE THIS FOR UPLOADING FILES!
    #@Slot()
    def open(self):
        self._ensure_stopped() # check playback was stopped
        file_dialog = QFileDialog(self) # opens a DIALOG



        movies_location = QStandardPaths.writableLocation(QStandardPaths.MoviesLocation)
        file_dialog.setDirectory(movies_location)

        if file_dialog.exec() == QDialog.Accepted:
            url = file_dialog.selectedUrls()[0]
            self._playlist.append(url)
            self._playlist_index = len(self._playlist) - 1
            self._player.setSource(url)
            self._player.play()



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'example_data'))
        print("setting path for data: ", self.data_path)

        self.setWindowTitle("My App")

        dialog_button = QPushButton("Press me for a dialog!")
        dialog_button.clicked.connect(self.dialog_button_clicked)

        self.setCentralWidget(dialog_button)


    def dialog_button_clicked(self, s):
        """
        you instance the dialog here. it runs on its own loop and freezes everythign else!
        NOTE: pass the parent name to the dialog!
        """
        print("dialog button clicked, toggled value: ", s)
        print("opening new dialog window")

        """        
        dlg = CustomDialog(self)
        dlg.setWindowTitle("HELLO!")
        
        # NOTE: fancy way of getting the values for accepted or rejected signals
        if dlg.exec_():
            print("Dialog accepted!")
        else: 
            print("Dialog rejected!")
        """
        
        # create file dialog
        file_dialog = QFileDialog(self)

        # checks supported types
        # use whatever filter the QFileDialog offers
        ...

        # set default directory
        ##location = 
        ##file_dialog.setDirectory(location)

        """
        using a static function: return a selected file 
            PySide6.QtWidgets.QFileDialog.getOpenFileName(...) https://doc.qt.io/qtforpython/PySide6/QtWidgets/QFileDialog.html#PySide6.QtWidgets.PySide6.QtWidgets.QFileDialog.getOpenFileName
            fileName = QFileDialog.getOpenFileName(self, tr("Open File"),() "/home", tr("Images (*.png *.xpm *.jpg)"))
            
            returns a tuple
                1) file path
                2) filter used 
                    QUESTION what are all filters available?

            the file if it was accepted, or a null string if rejected

        """
        file_name = QFileDialog.getOpenFileName(parent = self, caption = "Open File", dir = self.data_path, filter = "Images (*.png *.xpm *.jpg);;Text files (*.txt);;XML files (*.xml);;Audio (*.wav)")        

        if len(file_name[0])>0:
            print("a file was selected: ", file_name[0])
        else:
            print("No file was selected")

        ## run and check if it was accepted
        """
        if file_dialog.exec() == QDialog.Accepted:
            print("File selection accepted")
        """ 

def main():

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__=="__main__":
    main()