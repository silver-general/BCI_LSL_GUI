from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMainWindow

# Only needed for access to command line arguments
import sys

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window1 = QWidget()
window1.setWindowTitle("window1")
window1.show()  # IMPORTANT!!!!! Windows are hidden by default.

label = QLabel("some text!")
label.setWindowTitle("label")
label.show()

button = QPushButton("Push Me")
button.setWindowTitle("button")
button.show()

main_window = QMainWindow()
main_window.setWindowTitle("main window")
main_window.show()

# Start the event loop.
app.exec_()

# Your application won't reach here until you exit and the event
# loop has stopped.