import sys
from PySide6.QtWidgets import QApplication, QLabel

# sys.argv in case you pass command line arguments
app = QApplication(sys.argv)
# create a label object. can also use HTML!
label = QLabel("<font color=blue size=40>Hello World!</font>")
label.show()
app.exec()