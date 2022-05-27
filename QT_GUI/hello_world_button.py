"""
using a button click to display text on terminal
"""
def button_click_print():
    import sys
    from PySide6.QtWidgets import QApplication, QPushButton
    from PySide6.QtCore import Slot

    # Greetings
    @Slot() # NOTE: this function is decorated as a "slot"
    def say_hello():
        print("Button clicked, Hello!")


    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create a button
    button = QPushButton("Click me")

    # Connect the button to the function say_hello
    # button has a signal, clicked, that is triggered when it's clicked, and it can be connected through its connect method to a function 
    button.clicked.connect(say_hello)


    # Show the button
    button.show()
    # Run the main Qt loop
    app.exec()

#button_click_print()


"""

"""
def f():
    import sys
    from PySide6.QtWidgets import QApplication, QPushButton

    def function():
        print("The 'function' has been called!")

    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    #app = QApplication()
    button = QPushButton("Call function")
    button.clicked.connect(function)
    button.show()
    sys.exit(app.exec())

f()





