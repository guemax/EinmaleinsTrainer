import random

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        numbers()
        qLabelText = QLabel(f'Was ist {number1} * {number2}?', alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        font = qLabelText.font()
        font.setPointSize(20)
        qLabelText.setFont(font)

        # Set the window's name and size
        self.setWindowTitle("Einmaleins Trainer")
        self.setFixedSize(QSize(500, 400))

        self.setCentralWidget(qLabelText)


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
