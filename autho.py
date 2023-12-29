import json

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


def register_user(users):
    username = input("Введите имя пользователя: ")
    if username in users:
        print("Это имя пользователя уже занято. Попробуйте другое.")
        return None

    password = input("Введите пароль: ")
    users[username] = password
    save_users(users)
    print(f"Пользователь {username} успешно зарегистрирован.")
    return username


def login_user(users):
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")

    if username in users and users[username] == password:
        return username
    else:
        print("Неверное имя пользователя или пароль.")
        return None
