import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QWidget, QMessageBox, QDialog, QListWidget
from autho import AuthWindow

NOTES_FILE = "notes.json"


class NotesApp(QMainWindow):
    def __init__(self, username, auth_app):
        super().__init__()
        self.username = username
        self.auth_app = auth_app
        self.notes = self.load_notes()  # Загрузка заметок из файла
        self.initUI()

    def load_notes(self):
        try:
            with open(NOTES_FILE, 'r') as file:
                return json.load(file).get(self.username, [])
        except FileNotFoundError:
            return []

    def save_notes(self):
        try:
            with open(NOTES_FILE, 'r') as file:
                all_notes = json.load(file)
        except FileNotFoundError:
            all_notes = {}
        all_notes[self.username] = self.notes
        with open(NOTES_FILE, 'w') as file:
            json.dump(all_notes, file)

    def initUI(self):
        self.setWindowTitle("Заметки - " + self.username)
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.notes_list = QListWidget(self)
        layout.addWidget(self.notes_list)

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Введите заметку здесь...")  # Установка подсказки
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
