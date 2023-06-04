import random

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit
from PySide6.QtGui import QIntValidator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.question_widget = self.__init_question_widget()
        self.answer_widget = self.__init_answer_widget()
        self.result_widget = self.__init_result_widget()
        self.score_widget = self.__init_score_widget()

        # Init events
        self.answer_widget.returnPressed.connect(self.show_results)

        # Set the window's name and size
        self.setWindowTitle("Einmaleins Trainer")
        self.setFixedSize(QSize(500, 400))

        self.setCentralWidget(self.question_widget)

        self.first_factor = 0
        self.second_factor = 0
        self.product = 0

        self.correct_answer = 0
        self.false_answer = 0

        # Ask first question
        self.set_newly_generated_factors_and_product()
        self.ask_question(self.first_factor, self.second_factor)

    @staticmethod
    def __init_question_widget() -> QLabel:
        widget = QLabel(alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        font = widget.font()
        font.setPointSize(20)
        widget.setFont(font)

        return widget

    def ask_question(self, first_factor: int, second_factor: int) -> None:
        self.question_widget.setText(f'Was ist {first_factor} * {second_factor}?')

    def set_newly_generated_factors_and_product(self) -> None:
        factors, self.product = generate_factors_and_product()
        self.first_factor, self.second_factor = factors

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

    def __init_result_widget(self) -> QLabel:
        widget = QLabel(self, alignment=Qt.AlignmentFlag.AlignHCenter)
        widget.setFixedSize(500, 25)
        widget.move(Qt.AlignmentFlag.AlignHCenter, 140)

        font = widget.font()
        font.setPointSize(15)
        widget.setFont(font)

        return widget

    def __init_score_widget(self) -> QLabel:
        widget = QLabel(self, alignment=Qt.AlignmentFlag.AlignHCenter)
        widget.setFixedSize(500, 60)
        widget.move(Qt.AlignmentFlag.AlignHCenter, 200)

        font = widget.font()
        font.setPointSize(15)
        widget.setFont(font)

        return widget

    def show_results(self) -> None:
        answer = int(self.answer_widget.text())
        expected_answer = self.product

        if answer == expected_answer:
            self.result_widget.setText('Das ist richtig!')
            self.correct_answer += 1
        else:
            self.result_widget.setText(f'Die richtige Antwort wäre {expected_answer} gewesen.')
            self.false_answer += 1

        self.set_newly_generated_factors_and_product()
        self.ask_question(self.first_factor, self.second_factor)
        self.answer_widget.setText("")

        self.score_widget.setText(f'Richtige Antworten: {self.correct_answer}\nFalsche Antworten: {self.false_answer}')


def generate_factors_and_product() -> ((int, int), int):
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
