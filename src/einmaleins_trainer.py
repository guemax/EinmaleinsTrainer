import random

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window's name and size
        self.setWindowTitle("Einmaleins Trainer")
        self.setFixedSize(QSize(500, 400))


def numbers():
    global number1, number2
    number1 = random.randint(0, 20)
    number2 = random.randint(0, 20)


app = QApplication([])

# Create the window
window = MainWindow()
window.show()

# Start the event loop
app.exec()
