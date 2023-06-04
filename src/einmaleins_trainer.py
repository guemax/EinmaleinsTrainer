import random

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit
from PySide6.QtGui import QIntValidator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        generate_factors()

        question_widget = QLabel(f'Was ist {first_factor} * {second_factor}?', alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        font = question_widget.font()
        font.setPointSize(20)
        question_widget.setFont(font)

        self.answer_widget = QLineEdit(self)
        self.answer_widget.setMaxLength(3)
        self.answer_widget.move(225, 75)
        font = self.answer_widget.font()
        font.setPointSize(15)
        self.answer_widget.setFont(font)
        self.answer_widget.setFixedSize(40, 25)
        self.only_allow_integers = QIntValidator(self)
        self.answer_widget.setValidator(self.only_allow_integers)
        self.answer_widget.returnPressed.connect(self.validate_answer)

        # Set the window's name and size
        self.setWindowTitle("Einmaleins Trainer")
        self.setFixedSize(QSize(500, 400))

        self.setCentralWidget(question_widget)

    def validate_answer(self):
        print("Return pressed!")
        user_result = self.answer_widget.text()


def generate_factors():
    global first_factor, second_factor, product
    first_factor = random.randint(0, 20)
    second_factor = random.randint(0, 20)
    product = first_factor * second_factor


app = QApplication([])

# Create the window
window = MainWindow()
window.show()

# Start the event loop
app.exec()
