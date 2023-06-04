import random

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit
from PySide6.QtGui import QIntValidator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        factors, self.product = generate_factors()
        self.first_factor, self.second_factor = factors

        self.question_widget = self.__init_question_widget(self.first_factor, self.second_factor)
        self.answer_widget = self.__init_answer_widget()

        # Init events
        self.answer_widget.returnPressed.connect(self.validate_answer)

        # Set the window's name and size
        self.setWindowTitle("Einmaleins Trainer")
        self.setFixedSize(QSize(500, 400))

        self.setCentralWidget(self.question_widget)

    @staticmethod
    def __init_question_widget(first_factor:int, second_factor: int) -> QLabel:
        widget = QLabel(f'Was ist {first_factor} * {second_factor}?',
                        alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        font = widget.font()
        font.setPointSize(20)
        widget.setFont(font)

        return widget

    def __init_answer_widget(self) -> QLineEdit:
        widget = QLineEdit(self)
        widget.setMaxLength(3)
        widget.move(225, 75)
        widget.setFixedSize(40, 25)

        font = widget.font()
        font.setPointSize(15)
        widget.setFont(font)

        widget.setValidator(QIntValidator(self))

        return widget


    def validate_answer(self):
        print("Return pressed!")
        user_result = self.answer_widget.text()


def generate_factors() -> ((int, int), int):
    first_factor = random.randint(0, 20)
    second_factor = random.randint(0, 20)
    product = first_factor * second_factor

    return (first_factor, second_factor), product


app = QApplication([])

# Create the window
window = MainWindow()
window.show()

# Start the event loop
app.exec()
