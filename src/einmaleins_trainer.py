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
import json
import os
import platformdirs

from PySide6.QtCore import QSize, Qt, QUrl
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QWidget, QGridLayout, QPushButton, QDialog,\
    QDialogButtonBox
from PySide6.QtGui import QIntValidator, QPalette, QColor, QFont, QFontDatabase, QIcon, QAction
from PySide6.QtMultimedia import QSoundEffect

basedir = os.path.dirname(__file__)

appname = "Einmaleins Trainer"
appauthor = "PingTech"
values_path = platformdirs.user_data_dir(appname, appauthor, roaming=True, ensure_exists=True)

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'com.PingTech.EinmaleinsTrainer.0.1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class ResetHighscoreDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        QFontDatabase.addApplicationFont("ARLRDBD.TTF")

        self.setWindowTitle("Zurücksetzen bestätigen")

        self.buttons = QDialogButtonBox.Yes | QDialogButtonBox.No

        self.buttonBox = QDialogButtonBox(self.buttons)
        self.buttonBox.setStyleSheet(
            "QPushButton {"
            "background-color: #46515B;"
            "color: #FFEAEE;"
            "border-style: outset;"
            "border-width: 3px;"
            "border-radius: 10px;"
            "padding: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #2D353B;"
            "}"
            "QPushButton:pressed {"
            "background-color: #181C20;"
            "}"
        )
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.dialog_question_widget = self.__init_dialog_question_widget()

        layout = QGridLayout()

        layout.addWidget(self.dialog_question_widget, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.buttonBox, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        self.setStyleSheet(
            "QDialog {"
            "background-color: #798897;"
            "}"
            "QLabel {"
            "color: #FFEAEE;"
            "}"
        )

    @staticmethod
    def __init_dialog_question_widget() -> QLabel:
        widget = QLabel("Sind Sie sich sicher,dass Sie die Höchstpunktzahl\nzurücksetzen möchten? Dabei geht auch Ihr\n\
jetziger Spielstand verloren!")
        widget.setFont(QFont("Arial Rounded MT Bold", 10))

        return widget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.correct_answer_sound = "extra/correct_answer.wav"
        self.false_answer_sound = "extra/false_answer.wav"

        self.sound_effect_one = QSoundEffect()
        self.sound_effect_two = QSoundEffect()

        self.sound_effect_one.setSource(QUrl.fromLocalFile(self.correct_answer_sound))
        self.sound_effect_two.setSource(QUrl.fromLocalFile(self.false_answer_sound))
        self.sound_effect_one.setLoopCount(0)
        self.sound_effect_two.setLoopCount(0)

        self.question_widget = self.__init_question_widget()
        self.answer_widget = self.__init_answer_widget()
        self.result_widget = self.__init_result_widget()
        self.score_widget = self.__init_score_widget()
        self.exit_widget = self.__init_exit_widget()
        self.highscore_widget = self.__init_highscore_widget()

        # Init events
        self.answer_widget.returnPressed.connect(self.show_results)
        self.answer_widget.returnPressed.connect(self.update_highscore_widget)

        # Set the window's name and size
        self.setWindowTitle("Einmaleins Trainer")
        self.setFixedSize(QSize(500, 400))

        QFontDatabase.addApplicationFont("ARLRDBD.TTF")

        layout = QGridLayout()

        layout.addWidget(self.question_widget, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.answer_widget, 1, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.result_widget, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.score_widget, 3, 0, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.highscore_widget, 5, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.exit_widget, 6, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.button_set_sound = QAction(QIcon("extra/sound_on.ico"), "Ton", self)
        self.button_set_sound.triggered.connect(self.on_button_set_sound_click)
        self.button_set_sound.setCheckable(True)
        self.button_set_sound.setChecked(True)

        self.button_reset_highscore = QAction("Höchstpunktzahl zurücksetzen", self)
        self.button_reset_highscore.triggered.connect(self.on_button_reset_highscore_click)

        menu = self.menuBar()

        file_menu = menu.addMenu("&Einstellungen")
        file_menu.addAction(self.button_set_sound)
        file_menu.addAction(self.button_reset_highscore)

        self.first_factor = 0
        self.second_factor = 0
        self.product = 0

        self.correct_answer = 0
        self.false_answer = 0
        # self.saved_correct_answer = 0
        # self.saved_false_answer = 0

        self.sound_status = True

        self.load_values()
        self.update_highscore_widget()

        # Ask first question
        self.set_newly_generated_factors_and_product()
        self.ask_question(self.first_factor, self.second_factor)

    def on_button_set_sound_click(self) -> None:
        if self.button_set_sound.isChecked():
            self.sound_status = True
        else:
            self.sound_status = False

    def on_button_reset_highscore_click(self) -> None:
        dialog = ResetHighscoreDialog(self)
        if dialog.exec():
            self.correct_answer = 0
            self.false_answer = 0
            self.save_values()
            self.load_values()
            self.update_highscore_widget()
        else:
            pass

    @staticmethod
    def __init_question_widget() -> QLabel:
        widget = QLabel(alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        widget.setFont(QFont("Arial Rounded MT Bold", 20))

        return widget

    def ask_question(self, first_factor: int, second_factor: int) -> None:
        self.question_widget.setText(f'Was ist {first_factor} * {second_factor}?')

    def set_newly_generated_factors_and_product(self) -> None:
        factors, self.product = generate_factors_and_product()
        self.first_factor, self.second_factor = factors

    def __init_answer_widget(self) -> QLineEdit:
        widget = QLineEdit(self)
        widget.setMaxLength(3)
        widget.setFixedSize(55, 30)
        widget.setFont(QFont("Arial Rounded MT Bold", 15))
        widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        widget.setValidator(QIntValidator(self))

        widget.setStyleSheet("QLineEdit {"
                             "background-color: #46515B;"
                             "color: #FFEAEE;"
                             "border-style: outset;"
                             "border-width: 3px;"
                             "border-radius: 10px;"
                             "padding: 5px;"
                             "selection-background-color: #FFEAEE;"
                             "selection-color: #798897;"
                             "}"
                             "QLineEdit:focus {"
                             "border: 2px solid #FFEAEE;"
                             "}"
                             )

        return widget

    def __init_result_widget(self) -> QLabel:
        widget = QLabel(self)
        widget.setFont(QFont("Arial Rounded MT Bold", 15))

        return widget

    def __init_score_widget(self) -> QLabel:
        widget = QLabel(self)
        widget.setFont(QFont("Arial Rounded MT Bold", 15))

        return widget

    def __init_exit_widget(self) -> QPushButton:
        widget = QPushButton("Übung Beenden", self)
        widget.setFont(QFont("Arial Rounded MT Bold", 15))
        widget.setStyleSheet("QPushButton {"
                             "background-color: #46515B;"
                             "color: #FFEAEE;"
                             "border-style: outset;"
                             "border-width: 3px;"
                             "border-radius: 10px;"
                             "padding: 5px;"
                             "}"
                             "QPushButton:hover {"
                             "background-color: #2D353B;"
                             "}"
                             "QPushButton:pressed {"
                             "background-color: #181C20;"
                             "}"
                             )

        widget.clicked.connect(self.close)

        return widget

    def __init_highscore_widget(self) -> QLabel:
        widget = QLabel(self)
        widget.setFont(QFont("Arial Rounded MT Bold", 15))

        return widget

    def show_results(self) -> None:
        answer = int(self.answer_widget.text())
        expected_answer = self.product

        if answer == expected_answer:
            self.result_widget.setText('Das ist richtig!')
            self.correct_answer += 1
            if self.sound_status:
                self.sound_effect_one.play()
        else:
            self.result_widget.setText(f'Die richtige Antwort wäre {expected_answer} gewesen.')
            self.false_answer += 1
            self.correct_answer = max(self.correct_answer - 1, 0)
            if self.sound_status:
                self.sound_effect_two.play()

        self.set_newly_generated_factors_and_product()
        self.ask_question(self.first_factor, self.second_factor)
        self.answer_widget.setText("")

        self.score_widget.setText(f'<font color="#A7ED90">Richtige Antworten: {self.correct_answer}'
                                  f'</font><br><font color="#FF5159">Falsche Antworten: {self.false_answer}</font>')

    def closeEvent(self, event):
        # Save the values on application close
        if self.correct_answer > self.saved_correct_answer:
            self.save_values()
        event.accept()

    def load_values(self):
        try:
            # Load the values from a JSON file (if available)
            with open(os.path.join(values_path, 'values.json'), "r") as file:
                data = json.load(file)
                self.saved_correct_answer = data["correct_answer"]
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or there is an error in reading,
            # set the values to 0
            self.saved_correct_answer = 0

    def save_values(self):
        # Save the values in a JSON file
        data = {
            "correct_answer": self.correct_answer,
        }
        with open(os.path.join(values_path, 'values.json'), "w") as file:
            json.dump(data, file)

    def update_highscore_widget(self):
        # Update the text in the QLabel
        if self.correct_answer > self.saved_correct_answer:
            self.saved_correct_answer = self.correct_answer
            self.save_values()
        self.highscore_widget.setText(f"Höchstpunktzahl: {self.saved_correct_answer}")


def generate_factors_and_product() -> ((int, int), int):
    first_factor = random.randint(0, 20)
    second_factor = random.randint(0, 20)
    product = first_factor * second_factor

    return (first_factor, second_factor), product


app = QApplication([])
app.setWindowIcon(QIcon(os.path.join(basedir, 'extra', 'appico.ico')))
# Set global stylesheet
app.setStyleSheet(
    "QMainWindow {"
    "background-color: #798897;"
    "}"
    "QLabel {"
    "color: #FFEAEE;"
    "}"
    "QLineEdit {"
    "background-color: #798897;"
    "color: #FFEAEE;"
    "border-radius: 25px;"
    "padding: 5px;"
    "}"
    "QLineEdit:focus {"
    "border: 1px solid #FFEAEE;"
    "color: #FFEAEE;"
    "}"
)

# Create the window
window = MainWindow()
window.show()

# Start the event loop
app.exec()
