"""
using parts of
media player: https://doc.qt.io/qtforpython/examples/example_multimedia__player.html

creating the main window
    https://doc.qt.io/qtforpython/PySide6/QtWidgets/QMainWindow.html

"""

import sys

from PySide6.QtCore import QStandardPaths, Qt, Slot

from PySide6.QtGui import QAction, QIcon, QKeySequence, QScreen

from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog, QMainWindow, QSlider, QStyle, QToolBar)
from PySide6.QtWidgets import QPushButton


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        tool_bar = QToolBar()
        self.addToolBar(tool_bar)

        file_menu = self.menuBar().addMenu("&File")

        icon = QIcon.fromTheme("document-open")
        open_action = QAction(icon, "&Open...", self, shortcut=QKeySequence.Open, triggered=self.open)
        
        file_menu.addAction(open_action)
        tool_bar.addAction(open_action)
        
        icon = QIcon.fromTheme("application-exit")
        
        exit_action = QAction(icon, "E&xit", self,
                              shortcut="Ctrl+Q", triggered=self.close)
        
        file_menu.addAction(exit_action)

        about_menu = self.menuBar().addMenu("&About")

        about_qt_act = QAction("About &Qt", self, triggered=qApp.aboutQt)
        about_menu.addAction(about_qt_act)

        self._mime_types = []

    def closeEvent(self, event):
        self._ensure_stopped()
        event.accept()

    @Slot()
    def open(self):
        self._ensure_stopped()
        file_dialog = QFileDialog(self)

        is_windows = sys.platform == 'win32'
        if not self._mime_types:
            self._mime_types = get_supported_mime_types()
            if (is_windows and AVI not in self._mime_types):
                self._mime_types.append(AVI)
            elif MP4 not in self._mime_types:
                self._mime_types.append(MP4)

        file_dialog.setMimeTypeFilters(self._mime_types)

        default_mimetype = AVI if is_windows else MP4
        if default_mimetype in self._mime_types:
            file_dialog.selectMimeTypeFilter(default_mimetype)

        movies_location = QStandardPaths.writableLocation(QStandardPaths.MoviesLocation)
        file_dialog.setDirectory(movies_location)
        if file_dialog.exec() == QDialog.Accepted:
            url = file_dialog.selectedUrls()[0]
            self._playlist.append(url)
            self._playlist_index = len(self._playlist) - 1
            self._player.setSource(url)
            self._player.play()


if __name__ == '__main__':

    # instantiate Qapplication object
    app = QApplication(sys.argv)
    # create a main window 
    main_win = MainWindow()
    available_geometry = main_win.screen().availableGeometry()
    main_win.resize(available_geometry.width() / 3, available_geometry.height() / 2)
    main_win.show()
    sys.exit(app.exec())