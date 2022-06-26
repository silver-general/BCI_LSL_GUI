import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QSpinBox, QDoubleSpinBox, 
    QSlider, QDial
)
from PySide6.QtCore import Qt, QSize

from PySide6.QtGui import QPixmap

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        """
        widget: QLabel
            displays text
            OR an image if you pass
                display an image using .setPixmap(). This accepts an pixmap, which you can create by passing an image filename to QPixmap
                EG: widget.setPixmap(QPixmap('otje.jpg'))
        """
        label_01 = QLabel("some text")
        # changing text
        label_01.setText("New text")
        # setting a QLabel font: create a font object, setup options, set font
        font_01 = label_01.font()
        font_01.setPointSize(30)
        label_01.setFont(font_01)


        """
        alignments: use "horizontal | vertical" or just "Qt.AlignCenter" (Centers horizontally and vertically)
            horizontal
                Qt.AlignLeft 	Aligns with the left edge.
                Qt.AlignRight 	Aligns with the right edge.
                Qt.AlignHCenter 	Centers horizontally in the available space.
                Qt.AlignJustify 	Justifies the text in the available space.
            ---------------------------------------
            vertical
                Qt.AlignTop 	Aligns with the top.
                Qt.AlignBottom 	Aligns with the bottom.
                Qt.AlignVCenter 	Centers vertically in the available space.
            both
                Qt.AlignCenter 	Centers horizontally and vertically
        """
        label_01.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        label_02 = QLabel()
        label_02.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label_02.setPixmap(QPixmap("dog.png"))
        label_02.resize(QSize(5,5)) # cannot resize. why?

        # set central widget in the QMainWindow
        self.setCentralWidget(label_01)
        # (overrides the previous widget!)
        self.setCentralWidget(label_02)

        """
        widget: QCheckBox
            checkbox
            you can use it's state as follows
                QCheckBox.setCheckState(state)
                    state can be Qt.Checked or Qt.Unchecked
            making it tristate:
                If you set the value to Qt.PartiallyChecked the checkbox will become tristate. 
                You can also set a checkbox to be tri-state without setting the current state to partially checked by using .setTriState(True)
                values sent when state changes become 0, 1, 2
        """
        checkbox_01 = QCheckBox()
        # starts unchecked
        checkbox_01.setCheckState(Qt.Unchecked)
        # connect signal that happens when its state changes
        checkbox_01.stateChanged.connect(self.checkbox_01_showstate)
        # add as central widget
        self.setCentralWidget(checkbox_01)


        """
        widget: QComboBox
            drop down list
            currently selected item is the widget label
            passing items
                QComboBox.addItems() and pass a list of strings
            making it editable
                widget.setEditable(True)
                    # how to use this exactly??????????????????????????????????????
            choose how items are inserted
                widget.setInsertPolicy(QComboBox.InsertAlphabetically)
                and use any of the options
                    QComboBox.NoInsert 	            No insert
                    QComboBox.InsertAtTop 	        Insert as first item
                    QComboBox.InsertAtCurrent   	Replace currently selected item
                    QComboBox.InsertAtBottom    	Insert after last item
                    QComboBox.InsertAfterCurrent 	Insert after current item
                    QComboBox.InsertBeforeCurrent 	Insert before current item
                    QComboBox.InsertAlphabetically 	Insert in alphabetical order
            limit number of elements
                widget.setMaxCount(10)
            signals
                .currentIndexChanged: when the currently selected item is updated
                    passes the index of the chosen element
                .currentTextChanged: when the text changes
                    passes the string   
        """
        combo_01 = QComboBox()
        combo_01.setMaxCount(5) 
        combo_items = ["name1","name2","name3","name4","name5","name6"]
        combo_01.addItems(combo_items)
        # connect signals
        combo_01.currentIndexChanged.connect(self.combo_01_index_changed)
        combo_01.currentTextChanged.connect(self.combo_01_text_changed)
        # set editable
        ##combo_01.setEditable(True)
        self.setCentralWidget(combo_01)


        """
        widget: QListWidget
        
            add item: .addItem() with a list of items as parameters
            remove item: https://doc.qt.io/qtforpython/PySide6/QtWidgets/QListWidget.html#PySide6.QtWidgets.PySide6.QtWidgets.QListWidget.takeItem
                .takeItem()
                    with index of row to remove
            remove all items:
                .clear()
            get current item index:
                to get the INDEX: https://doc.qt.io/qtforpython/PySide6/QtWidgets/QListWidget.html#PySide6.QtWidgets.PySide6.QtWidgets.QListWidget.currentRow
                
                in addition
                    .currentItem() returns a QListWidgetItem https://doc.qt.io/qtforpython/PySide6/QtWidgets/QListWidgetItem.html#PySide6.QtWidgets.PySide6.QtWidgets.QListWidgetItem.text
                    to get the text, go for QListWidgetItem.text()
                        basicall: .currentItem().text()
               
            signals:
                currentItemChanged signal which sends the QListItem (!!!)
                currentTextChanged signal which sends the text
        """
        list_01 = QListWidget()
        list_items = ["name1","name2","name3","name4","name5","name6"]
        list_01.addItems(list_items)

        list_01.currentItemChanged.connect( self.list_01_item_changed )
        list_01.currentTextChanged.connect( self.list_01_text_changed )

        self.setCentralWidget(list_01)


        """
        widget: QLineEdit
            allows user to modify text in a box

            signals
                - when return is pressed. doesn't pass anything!
                - 
                - user edits
                - another program part edits

        """
        line_edit_01 = QLineEdit("text")
        line_edit_01.setMaxLength(10)
        line_edit_01.setPlaceholderText("Enter your text")
        # setup signals
        line_edit_01.returnPressed.connect(self.line_edit_01_return_pressed)
        line_edit_01.selectionChanged.connect(self.line_edit_01_selection_changed)
        line_edit_01.textChanged.connect(self.line_edit_01_text_changed) # user edits!
        line_edit_01.textEdited.connect(self.line_edit_01_text_edited) # another part of the program edits!

        self.setCentralWidget(line_edit_01)


        """
        widget: QSpinbox or QDoubleSpinbox

        signals:
            - value changes, passes value as number
            - text changes, passes value as string
        """
        spinbox_01 = QSpinBox()
            # Or: widget = QDoubleSpinBox() is you want to use floating points!
        spinbox_01.setMinimum(-10)
        spinbox_01.setMaximum(3)
            # Or: widget.setRange(-10,3)
        spinbox_01.setPrefix("$")
        spinbox_01.setSuffix("c")
        spinbox_01.setSingleStep(3)  # Or e.g. 0.5 for QDoubleSpinBox
        spinbox_01.valueChanged.connect(self.spinbox_01_value_changed) #  passes a value
        spinbox_01.textChanged.connect(self.spinbox_01_value_changed_str) #  passes a string!

        self.setCentralWidget(spinbox_01)

        """
        widget: QSlider
        """
        slider_01 = QSlider(Qt.Vertical)
            # OR: slider_01.QSlider(Qt.Horizontal)
        slider_01.setMinimum(0)
        slider_01.setMaximum(10)
            # Or: slider_01.setRange(-10,3)

        slider_01.setSingleStep(2)

        slider_01.valueChanged.connect(self.slider_01_value_changed)
        slider_01.sliderMoved.connect(self.slider_01_slider_position)
        slider_01.sliderPressed.connect(self.slider_01_slider_pressed)
        slider_01.sliderReleased.connect(self.slider_01_slider_released)

        self.setCentralWidget(slider_01)


        """
        widget: QDial

        signals:
            - value changes, passes the value
            - slider moves, passes value
            - slider pressed
            - slider released
        """
        dial_01 = QDial()
        dial_01.setRange(-10, 100)
        dial_01.setSingleStep(0.5)

        dial_01.valueChanged.connect(self.dial_01_value_changed)
        dial_01.sliderMoved.connect(self.dial_01_slider_position)
        dial_01.sliderPressed.connect(self.dial_01_slider_pressed)
        dial_01.sliderReleased.connect(self.dial_01_slider_released)

        self.setCentralWidget(dial_01)


    def checkbox_01_showstate(self,state):
        """
        when checkbox_01 changes state, its signal activates this
        note that the signal sends 0 or 2!
        """
        if state==0:
            print("checkbox_01 unchecked! signal value: {}".format(state))
        else:
            print("checkbox_01 checked! signal value: {}".format(state))
 
    def combo_01_index_changed(self,i):
        print("combo_01 index changed. value is {}".format(i))
    def combo_01_text_changed(self,text):
        print("combo_01 text changed. text is: {}".format(text))

    def list_01_item_changed(self,item):
        """
        INPUT
            item: it's the QListItem object!
        """
        print("list_01 item changed. item is: {}".format(item))
    def list_01_text_changed(self,text):
        print("list_01 text changed. text is: {}".format(text))

    def line_edit_01_return_pressed(self):
        print("Return pressed!")
        self.centralWidget().setText("BOOM!")
    def line_edit_01_selection_changed(self):
        print("Selection changed")
        print(self.centralWidget().selectedText())
    def line_edit_01_text_changed(self, s):
        # NOTE: returns the string too!
        print("Text changed (programmatic change)...")
        print(s)
    def line_edit_01_text_edited(self, s):
        # NOTE: only when user edits text! returns the string too!
        print("Text edited (user edit)...")
        print(s)

    def spinbox_01_value_changed(self, i):
        print(i)
    def spinbox_01_value_changed_str(self, s):
        print(s)

    def slider_01_value_changed(self, i):
        # value as parameter
        print(i)
    def slider_01_slider_position(self, p):
        print("position", p)
    def slider_01_slider_pressed(self):
        print("Pressed!")
    def slider_01_slider_released(self):
        print("Released")

    def dial_01_value_changed(self, i):
        print(i)
    def dial_01_slider_position(self, p):
        print("position", p)
    def dial_01_slider_pressed(self):
        print("Pressed!")
    def dial_01_slider_released(self):
        print("Released")


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()