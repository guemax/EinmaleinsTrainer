import random

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit
from PySide6.QtGui import QIntValidator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        numbers()
        q_label_text = QLabel(f'Was ist {number_one} * {number_two}?', alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        font = q_label_text.font()
        font.setPointSize(20)
        q_label_text.setFont(font)

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

        self.setCentralWidget(q_label_text)

    def return_pressed(self):
        print("Return pressed!")
        user_result = self.input.text()


def numbers():
    global number_one, number_two, expected_result
    number_one = random.randint(0, 20)
    number_two = random.randint(0, 20)
    expected_result = number_one * number_two


app = QApplication([])

# Create the window
window = MainWindow()
window.show()

# Start the event loop
app.exec()
