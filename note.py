import json
import autho

NOTES_FILE = "notes.json"

def load_notes():
    try:
        with open(NOTES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_notes(notes):
    with open(NOTES_FILE, 'w') as file:
        json.dump(notes, file)

def add_note(notes, username):
    note = input("Введите заметку: ")
    notes.setdefault(username, []).append(note)
    save_notes(notes)
    print("Заметка добавлена.")

def look_notes(notes, username):
    user_notes = notes.get(username, [])
    if user_notes:
        for i, note in enumerate(user_notes, start=1):
            print(f"{i}) {note}")
    else:
        print("У вас пока нет заметок.")

def main_menu():
    users = autho.load_users()
    notes = load_notes()

    while True:
        print("\n1) Регистрация\n2) Вход\n3) Выход")
        choice = input("Выберите действие: ")
        if choice == "1":
            username = autho.register_user(users)
        elif choice == "2":
            username = autho.login_user(users)
        elif choice == "3":
            break
        else:
            print("Введите корректно!\n")

        if username:
            while True:
                print(f"\nПривет, {username}!\n"
                      "1) Добавить заметку\n"
                      "2) Посмотреть заметки\n"
                      "3) Выход\n")
                user_choice = input("Выберите действие: ")
                if user_choice == "1":
                    add_note(notes, username)
                elif user_choice == "2":
                    look_notes(notes, username)
                elif user_choice == "3":
                    break
                else:
                    print("Введите корректно!\n")

if __name__ == "__main__":
    main_menu()
