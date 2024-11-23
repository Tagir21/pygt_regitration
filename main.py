from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from registration import NewUserDialog

import sys

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initialiseUI()

    def initialiseUI(self):
        self.setFixedSize(360, 220)
        self.setWindowTitle("Login window")

        self.setUpWindow()
        self.show()

    def setUpWindow(self):

        self.login_is_successful = False

        login_label = QLabel("Login", self)
        login_label.setFont(QFont("Arial", 20))
        login_label.move(160, 10)

        username_label = QLabel("Имя пользователя:", self)
        username_label.move(20, 54)

        self.username_edit = QLineEdit(self)
        self.username_edit.resize(250, 24)
        self.username_edit.move(90, 50)
        password_label = QLabel("Пароль:", self)
        password_label.move(20, 86)

        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.resize(250, 24)
        self.password_edit.move(90, 82)

        self.show_password_cb = QCheckBox("Показать пароль", self)
        self.show_password_cb.move(90, 110)
        self.show_password_cb.toggled.connect(self.displayPasswordIfChecked)

        login_button = QPushButton("Login", self)
        login_button.resize(320, 34)
        login_button.move(20, 140)
        login_button.clicked.connect(self.clickLoginButton)

        not_member_label = QLabel("Не являетесь членом?", self)
        not_member_label.move(20, 186)

        sign_up_button = QPushButton("Зарегистрироваться", self)
        sign_up_button.move(120, 180)
        sign_up_button.clicked.connect(self.createNewUser)

    def clickLoginButton(self):
        users = {}
        file = "files/users.txt"
        try:
            with open(file, "r") as f:
                for line in f:
                    user_info = line.split(" ")
                    username_info = user_info[0]
                    password_info = user_info[1].strip("\n")
                    users[username_info] = password_info

            username = self.username_edit.text()
            password = self.password_edit.text()

            if (username, password) in users.items():
                QMessageBox.information(self, "Login Successful!",  "Login Successful!", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
                self.login_is_successful = True
                self.close()
                self.openApplicationWindow()
            else:
                QMessageBox.warning(self, "Сообщение об ошибке", "Имя пользователя или пароль неверны.", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
        except FileNotFoundError as error:
            QMessageBox.warning(self, "Ошибка",
                                f"""<p>Файл не найден.</p>
                                <p>Ошибка: {error}</p>""",
                                QMessageBox.StandardButton.Ok)
            f = open(file, "w")

    def displayPasswordIfChecked(self, checked):
        if checked:
            self.password_edit.setEchoMode(
                QLineEdit.EchoMode.Normal)
        elif checked == False:
            self.password_edit.setEchoMode(
                QLineEdit.EchoMode.Password)

    def createNewUser(self):
        self.create_new_user_window = NewUserDialog()
        self.create_new_user_window.show()

    def openApplicationWindow(self):
        self.main_window = MainWindow()
        self.main_window.show()

    def closeEvent(self, event):

        if self.login_is_successful == True:
            event.accept()
        else:
            answer = QMessageBox.question(
                self, "Выйти из приложения?",
                "Вы уверены, что хотите выйти из приложения?",
                QMessageBox.StandardButton.No | \
                QMessageBox.StandardButton.Yes,
                QMessageBox.StandardButton.Yes)
            if answer == QMessageBox.StandardButton.Yes:
                event.accept()
            if answer == QMessageBox.StandardButton.No:
                event.ignore()


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setMinimumSize(640, 426)
        self.setWindowTitle('3.1 - Главное окно')
        self.setUpMainWindow()

    def setUpMainWindow(self):
        image = "images/background_kingfisher.jpg"

        try:
            with open(image):
                main_label = QLabel(self)
                pixmap = QPixmap(image)
                main_label.setPixmap(pixmap)
                main_label.move(0, 0)
        except FileNotFoundError as error:
            print(f"Изображение не найдено.\nError: {error}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec_())
