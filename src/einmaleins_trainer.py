import random

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit
from PySide6.QtGui import QIntValidator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        numbers()
        qLabelText = QLabel(f'Was ist {number1} * {number2}?', alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        font = qLabelText.font()
        font.setPointSize(20)
        qLabelText.setFont(font)

        self.input = QLineEdit(self)
        self.input.setMaxLength(3)
        self.input.move(225, 75)
        font = self.input.font()
        font.setPointSize(15)
        self.input.setFont(font)
        self.input.setFixedSize(40, 25)
        self.onlyInt = QIntValidator(self)
        self.input.setValidator(self.onlyInt)
        self.input.returnPressed.connect(self.return_pressed)

        # Set the window's name and size
        self.setWindowTitle("Einmaleins Trainer")
        self.setFixedSize(QSize(500, 400))

        self.setCentralWidget(qLabelText)

    def return_pressed(self):
        print("Return pressed!")
        userResult = self.input.text()
        print(userResult)


def numbers():
    global number1, number2, expectedResult
    number1 = random.randint(0, 20)
    number2 = random.randint(0, 20)
    expectedResult = number1 * number2


app = QApplication([])

# Create the window
window = MainWindow()
window.show()

# Start the event loop
app.exec()
