notes = list()

def add_notes():
    note = input("\nВведите заметку: ")
    notes.append(note)


def look_notes():
    if not notes:
        print("\nПока что здесь заметок\n")
    else:
        for i, task in enumerate(notes, start=1):
            print(f"\n{i}) {task}")
        print()

def delete_notes():
    look_notes()
    try:
        usr_option = int(input("\nКакую заметку вы хотите удалить: ")) - 1
        if 0 <= usr_option < len(notes):
            del notes[usr_option]
            print("Заметка успешно удалена!")
        else:
            print("Такого индекса нет")
    except ValueError:
        print("Пожалуйста, введите число.")


def main_info():
    flag = True
    while flag:
        print("\n1) Добавить заметку\n"
              "2) Посмотреть заметку\n"
              "3) Удалить заметку\n"
              "4) Выход\n")
        usr_choice = input("\nВыберите цифру из меню: ")
        if usr_choice == "1":
            add_notes()
        elif usr_choice == "2":
            look_notes()
        elif usr_choice == "3":
            delete_notes()
        elif usr_choice == "4":
            flag = False

            print("Оцените пожалуйста наше приложение!\n"
                  "0 - это хорошо\n"
                  "1 - это плохо\n")
            grade = input("Ввод: ")
            if grade == "0":
                print("Спасибо. Мы очень рады!")
            elif grade == "1":
                print("Очень жаль(")
            else:
                print("Введите 0 или 1!")
                flag = False
            print("Спасибо что пользуетесь нашим приложением!")
        else:
            print("Введите корректно!\n")


if __name__ == "__main__":
    main_info()

