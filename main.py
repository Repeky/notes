import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QWidget, QMessageBox, \
    QDialog, QListWidget
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QByteArray
import base64
from autho import AuthWindow, encrypt_data, decrypt_data, load_key
import icon

NOTES_FILE = "notes.json"

# ico и для регестрации new дизайн
class NotesApp(QMainWindow):
    def __init__(self, username, auth_app):
        super().__init__()
        self.username = username
        self.auth_app = auth_app
        self.notes = self.load_notes()  # Загрузка заметок из файла
        self.initUI()
        self.update_notes_list()

    def load_notes(self):
        try:
            with open(NOTES_FILE, 'rb') as file:
                encrypted_data = file.read()
            decrypted_data = decrypt_data(encrypted_data)
            return json.loads(decrypted_data)
        except FileNotFoundError:
            return []

    def save_notes(self):
        data = json.dumps(self.notes)
        encrypted_data = encrypt_data(data)
        with open(NOTES_FILE, 'wb') as file:
            file.write(encrypted_data)

    def initUI(self):
        self.setWindowTitle("Заметки - " + self.username)
        self.setGeometry(300, 300, 600, 400)

        encoded_icon = icon.ico
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray.fromBase64(encoded_icon.encode()))
        self.setWindowIcon(QIcon(pixmap))

        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.notes_list = QListWidget(self)
        layout.addWidget(self.notes_list)

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Введите заметку здесь...")  # Установка подсказки
        self.text_edit.setStyleSheet("QTextEdit { background-color: #f0f0f0; border: 1px solid #ddd; border-radius: 5px; padding: 5px; }")
        layout.addWidget(self.text_edit)

        save_button = QPushButton("Сохранить заметку", self)
        save_button.clicked.connect(self.save_note)
        layout.addWidget(save_button)

        delete_note_button = QPushButton("Удалить заметку", self)
        delete_note_button.clicked.connect(self.delete_note)
        layout.addWidget(delete_note_button)

        switch_user_button = QPushButton("Сменить пользователя", self)
        switch_user_button.clicked.connect(self.switch_user)
        layout.addWidget(switch_user_button)

        exit_button = QPushButton("Выйти", self)
        exit_button.clicked.connect(self.exit_app)
        layout.addWidget(exit_button)

        self.setStyleSheet("QPushButton { background-color: #e7e7e7; border: none; border-radius: 3px; padding: 5px 10px; margin: 5px; } "
                           "QPushButton:hover { background-color: #d7d7d7; }")

    def save_note(self):
        note = self.text_edit.toPlainText()
        if note:
            self.notes.append(note)
            self.save_notes()  # Сохранение заметок в файл
            self.update_notes_list()
            QMessageBox.information(self, "Информация", "Заметка сохранена.")
            self.text_edit.clear()

    def new_note(self):
        self.text_edit.clear()

    def delete_note(self):
        selected_item = self.notes_list.currentRow()
        if selected_item >= 0:
            del self.notes[selected_item]
            self.save_notes()  # Сохранение после удаления заметки
            self.update_notes_list()

    def update_notes_list(self):
        self.notes_list.clear()
        self.notes_list.addItems(self.notes)

    def switch_user(self):
        self.close()
        self.auth_app.show()

    def exit_app(self):
        self.close()


def main():
    app = QApplication(sys.argv)

    auth_window = AuthWindow()
    if auth_window.exec() == QDialog.DialogCode.Accepted:
        main_window = NotesApp(auth_window.username_edit.text(), auth_window)
        main_window.show()
    else:
        sys.exit()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
