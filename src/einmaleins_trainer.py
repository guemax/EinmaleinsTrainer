"""MIT License

Copyright (c) 2023 guefra

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import random

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QWidget, QGridLayout
from PySide6.QtGui import QIntValidator, QPalette, QColor


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


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

        layout = QGridLayout()

        layout.addWidget(self.question_widget, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.answer_widget, 1, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.result_widget, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.score_widget, 3, 0, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(Color('orange'), 5, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

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
        widget.setFixedSize(40, 25)

        font = widget.font()
        font.setPointSize(15)
        widget.setFont(font)

        widget.setValidator(QIntValidator(self))

        return widget

    def __init_result_widget(self) -> QLabel:
        widget = QLabel(self)

        font = widget.font()
        font.setPointSize(15)
        widget.setFont(font)

        return widget

    def __init_score_widget(self) -> QLabel:
        widget = QLabel(self)

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
