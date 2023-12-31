import json
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QDialog)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QByteArray
from cryptography.fernet import Fernet
import os
import base64
import icon

USERS_FILE = "users.json"
KEY_FILE = "secret.key"



def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return key


def encrypt_data(data):
    key = load_key()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data


def decrypt_data(encrypted_data):
    key = load_key()
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data.decode()


def load_users():
    try:
        with open(USERS_FILE, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = decrypt_data(encrypted_data)
        return json.loads(decrypted_data)
    except FileNotFoundError:
        return {}


def save_users(users):
    data = json.dumps(users)
    encrypted_data = encrypt_data(data)
    with open(USERS_FILE, 'wb') as file:
        file.write(encrypted_data)


class AuthWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.users = load_users()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Авторизация / Регистрация")
        layout = QVBoxLayout()

        encoded_icon = icon.ico

        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray.fromBase64(encoded_icon.encode()))

        self.setWindowIcon(QIcon(pixmap))

        self.setStyleSheet("""
                    QDialog {
                        background-color: #f0f0f0;
                    }
                    QLineEdit {
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QPushButton {
                        background-color: #e7e7e7;
                        border: none;
                        border-radius: 3px;
                        padding: 5px 10px;
                        margin: 5px;
                    }
                    QPushButton:hover {
                        background-color: #d7d7d7;
                    }
                """)

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
