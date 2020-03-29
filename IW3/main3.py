import sys

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from RC5 import RC5

task = """№ 9. Реализовать программный продукт, позволяющий шифровать и
расшифровывать сообщения на русском языке с помощью RC5 для трех
различных вариантов. Чтение открытого текста и шифртекста должно быть
возможно с клавиатуры, запись результата шифрования/расшифрования на
экран. Ключ формируется автоматически и сохраняется на весь сеанс
шифрования. Ключ сохраняется в отдельный файл. Для реализации
криптоалгоритмов запрещено пользоваться встроенными библиотеками
используемых языков."""
CRYPT = 0
DECRYPT = 1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.source_text_widget = QTextEdit("текст который должен быть зашифрован")
        self.result_widget = QTextEdit()
        self.w_input_widget = QLineEdit("32")
        self.r_input_widget = QLineEdit("25")
        self.b_input_widget = QLineEdit("32")
        self.RC5 = None
        self.onlyInt = QIntValidator()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()

        self.w_input_widget.setValidator(self.onlyInt)
        self.r_input_widget.setValidator(self.onlyInt)
        self.b_input_widget.setValidator(self.onlyInt)
        self.w_input_widget.setMaximumWidth(50)
        self.r_input_widget.setMaximumWidth(50)
        self.b_input_widget.setMaximumWidth(50)
        self.source_text_widget.setMinimumWidth(300)
        self.result_widget.setMinimumWidth(300)
        self.result_widget.setMinimumHeight(150)
        self.source_text_widget.setMinimumHeight(150)
        self.result_widget.setReadOnly(True)

        button_encrypt = QPushButton("Шифровать")
        button_decrypt = QPushButton("Расшифровать")
        button_encrypt.clicked.connect(self.go_encrypt)
        button_decrypt.clicked.connect(self.go_decrypt)

        left_panel = QWidget()
        left_grid = QGridLayout(left_panel)
        left_grid.addWidget(QLabel("W:"), 0, 0)
        left_grid.addWidget(QLabel("R:"), 1, 0)
        left_grid.addWidget(QLabel("B:"), 2, 0)
        left_grid.addWidget(self.w_input_widget, 0, 1)
        left_grid.addWidget(self.r_input_widget, 1, 1)
        left_grid.addWidget(self.b_input_widget, 2, 1)

        hbox.addWidget(left_panel)

        right_panel = QWidget()
        right_grid = QGridLayout(right_panel)
        right_grid.addWidget(QLabel("Исходный текст:"), 0, 0)
        right_grid.addWidget(QLabel("Результат:"), 0, 1)
        right_grid.addWidget(self.source_text_widget, 1, 0)
        right_grid.addWidget(self.result_widget, 1, 1)
        right_grid.addWidget(button_encrypt, 2, 0)
        right_grid.addWidget(button_decrypt, 2, 1)

        hbox.addWidget(right_panel)
        self.mainWidget.setLayout(hbox)

    def getRC5(self, mode):
        key = None
        if self.RC5 is None:
            if mode == DECRYPT:
                key = self.get_key_from_file()
            if self.w_input_widget.text() and self.r_input_widget.text() and self.b_input_widget.text():
                if key is None:
                    self.RC5 = RC5(int(self.w_input_widget.text()), int(self.r_input_widget.text()),
                                   int(self.b_input_widget.text()))
                else:
                    self.RC5 = RC5(int(self.w_input_widget.text()), int(self.r_input_widget.text()),
                                   int(self.b_input_widget.text()), key)

                return True
            else:
                return False
        if self.RC5.w != int(self.w_input_widget.text()) or self.RC5.R != int(
                self.r_input_widget.text()) or self.RC5.b != int(self.b_input_widget.text()):
            self.RC5 = RC5(int(self.w_input_widget.text()), int(self.r_input_widget.text()),
                           int(self.b_input_widget.text()))
        return True

    def go_encrypt(self):
        if not self.preparation():
            return
        result = self.RC5.encryptBytes(self.source_text_widget.toPlainText().encode())
        self.result_widget.setText(result.decode('iso8859-1'))
        self.save_key()

    def save_key(self):
        with open("key.txt", "wb") as file:
            file.write(self.RC5.key)
        with open("result.txt", "wb") as file:
            file.write(self.result_widget.toPlainText().encode('iso8859-1'))

    def go_decrypt(self):
        if not self.preparation(mode=DECRYPT):
            return
        result = self.RC5.decryptBytes(self.source_text_widget.toPlainText().encode("iso8859-1"))
        self.result_widget.setText(result.decode())

    def preparation(self, mode=CRYPT):
        if not self.getRC5(mode):
            return
        if not self.source_text_widget.toPlainText().encode():
            return
        return True

    def get_key_from_file(self):
        # try:
        if not self.source_text_widget.toPlainText():
            with open("result.txt", "rb") as file:
                self.source_text_widget.setText(file.read().decode('iso8859-1'))
        with open("key.txt", "rb") as file:
            return file.read()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
