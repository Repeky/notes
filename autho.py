import json
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QDialog)

USERS_FILE = "users.json"

def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file)

class AuthWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.users = load_users()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Авторизация")
        self.setGeometry(300, 300, 200, 150)
        layout = QVBoxLayout()

        self.username_edit = QLineEdit(self)
        self.username_edit.setPlaceholderText("Имя пользователя")
        layout.addWidget(self.username_edit)

        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("Пароль")
        layout.addWidget(self.password_edit)

        login_button = QPushButton("Войти", self)
        login_button.clicked.connect(self.login_user)
        layout.addWidget(login_button)

        register_button = QPushButton("Регистрация", self)
        register_button.clicked.connect(self.register_user)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def login_user(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        if username in self.users and self.users[username] == password:
            QMessageBox.information(self, "Успех", "Вы успешно вошли в систему!")
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль.")

    def register_user(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return
        if username in self.users:
            QMessageBox.warning(self, "Ошибка", "Это имя пользователя уже занято.")
            return
        self.users[username] = password
        save_users(self.users)
        QMessageBox.information(self, "Успех", "Пользователь успешно зарегистрирован.")
