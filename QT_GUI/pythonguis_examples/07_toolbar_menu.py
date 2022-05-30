"""
TOOLBAR
    bar of icons sed to perform certain actions
    you can read this later https://www.pythonguis.com/tutorials/pyside6-actions-toolbars-menus/


    USING ACTIONS

"""



import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar, QCheckBox
)
from PySide6.QtGui import QAction, QIcon,QKeySequence
from PySide6.QtCore import Qt,QSize

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My Awesome App")

        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)

        """
        ADDING A TOOLBAR: QToolBar
            setups
                you can set icon size here
        """
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(30, 30)) 
        self.addToolBar(toolbar)

        """
        adding one QAction object to the toolbar
            creating an action
                pass icon,label, also pass "self" as LAST element
                NOTE: "label" is the string of text you see when you hover the mous on top, or on the button if there is no icon!
                    but: this depends on the operative system's default. you can change this by using .setToolButtonStyle(...) with parameter:
                        Qt.ToolButtonIconOnly       	Icon only, no text
                        Qt.ToolButtonTextOnly 	        Text only, no icon
                        Qt.ToolButtonTextBesideIcon 	Icon and text, with text beside the icon
                        Qt.ToolButtonTextUnderIcon 	    Icon and text, with text under the icon
                        Qt.ToolButtonFollowStyle 	    Follow the host desktop style
            setting a shortcut for an action
                exit_action.setShortcut(QKeySequence("Ctrl+q"))

            creating a separator 
               toolbar.addSeparator()

            signal:
                triggered: when clicked. also sends a flag depending on the "checked status" (False by default)   
            steps
                create QAction and setup behaviour: ".setStatusTip",".setCheckable" 
                connect signals: "triggered.connect"
                add it to toolbar: "toolbar.addAction(action)"
        
        A NOTE ON ICONS
            create QIcon, write path to png as parameter
            set it up: to resize icons, you have a setting in the toolbar object!
            pass it a first parameter when creating a QAction for the toolbar
        """

        # FIRST, an ICON
        icon_01 = QIcon("bug.png")
            # NOTE: this can go directly as first parameter in the following command.         

        # then, the action
        button_action = QAction(icon_01, "Your button", self) # NOTE: you are also passing the parent here (self), as FINAL argument!
            # NOTE: can also give a label as parameter
        # display text in status bar, if you have one
        button_action.setStatusTip("This is your button")
        # make it checkable
        button_action.setCheckable(True)        

        # signals
        button_action.triggered.connect(self.toolbar_button_01_clicked)

        # add action to toolbar
        toolbar.addAction(button_action)

        # separator between widget 1 and 2
        toolbar.addSeparator()

        # add second widget
        button_action2 = QAction(QIcon("cassette.png"), "Your Button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.toolbar_button_02_clicked)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        toolbar.addWidget(QLabel("Hello"))
        toolbar.addWidget(QCheckBox())

        self.setStatusBar(QStatusBar(self))



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
        MENUS
            add a menu bar: 
                self.menuBar(), with self being the mainwindow object you are initialising
            add a menu 
                (menu = an item on the menu bar):
                    .addMenu(), passing in the name of the menu
            To add an action to a menu 
                you call .addAction passing in one of our defined actions
                    this is the thing you are used to see when you do "file -> save". "save" is the action
            set shortcut for an action
                this is shown in the menu if you add the action!
                exit_action.setShortcut(QKeySequence("Ctrl+q"))
        """
        # create menu bar bu running a method of the QMainWindow
        menu = self.menuBar()
        # add an item to the menubar
        file_menu = menu.addMenu("File")
        #add a separator
        file_menu.addSeparator()
        """add something to the file menu, like an exit option (an action)"""
        exit_action = QAction(QIcon.fromTheme("application-exit"),"Quit", self) # first, define an action  
        # ADD A SHORTCUT 
        exit_action.setShortcut(QKeySequence("Ctrl+q"))
        exit_action.triggered.connect(self.exit_action_called)      
        file_menu.addAction(exit_action)

        # some more menu elements
        streams_menu = menu.addMenu("Streams")
        tools_menu = menu.addMenu("Tools")

        # nesting another menu
        view_menu = tools_menu.addMenu("View")
        # temporary action just for display
        dummy_action = QAction("this action doesn't do anything",self)
        # add it
        view_menu.addAction(dummy_action)

    def toolbar_button_01_clicked(self, s):
        print("click on 1.", s)    
    def toolbar_button_02_clicked(self, s):
        print("click on 2.", s)
    def exit_action_called(self):
        self.close()

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()















