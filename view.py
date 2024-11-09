
import time


class View:
    def show_menu(self):
        while True:
            print("Меню:")
            print("1. Вивід назв таблиць")
            print("2. Вивід імен стовпчиків таблиці")
            print("3. Додавання даних в таблицю")
            print("4. Оновлення даних в таблиці")
            print("5. Видалення даних в таблиці")
            print("6. Генерування даних в таблицю")
            print("7. Перегляд данних в таблиці")
            print("8. Знайти тренування по вазі користувача і назви вправи")
            print("9. Знайти вправу по кількості підходів і складністю")
            print("10. Знайти середні показники для тренувань по початку тренування")
            print("11. Вихід")

            choice = input("Зробіть вибір: ")

            if choice in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'):
                return choice
            else:
                print("Будь ласка, введіть правильний номер опції (від 1 до 11)")
                time.sleep(2)

    def show_message(self, message):
        print(message)
        time.sleep(2)

    def show_tables(self, tables):
        print("Назви таблиць:")
        for table in tables:
            print(table)
        time.sleep(2)

    def show_data(self, data: list, columns):
        for data_tuple in data:
            for i, el in enumerate(data_tuple):
                print(f'{columns[i]}: {el}', end=" ")
            print()
        time.sleep(2)

    def ask_table(self):
        table_name = input("Введіть назву таблиці: ")
        return table_name

    def show_columns(self, columns):
        print("Назви стовпців:")
        for column in columns:
            print(column)
        time.sleep(2)

    def insert(self):
        while True:
            try:
                table = input("Введіть назву таблиці: ")
                columns = input("Введіть назви колонок (через пробіл): ").split()
                val = input("Введіть відповідні значення (через пробіл): ").split()

                if len(columns) != len(val):
                    raise ValueError("Кількість стовпців повинна бути дорівнювати кількості значень.")

                return table, columns, val
            except ValueError as e:
                print(f"Помилка: {e}")

    def update(self):
        while True:
            try:
                table = input("Введіть назву таблиці: ")
                columns = input("Введіть назви колонок (через пробіл), які хочете змінити: ").strip().split()
                id = int(input("Введіть ID рядка, який потрібно змінити: "))
                new_values = input(f"Введіть {len(columns)} нових значень: ").split()
                return table, columns, id, new_values
            except ValueError as e:
                print(f"Помилка: {e}")

    def delete(self):
        while True:
            try:
                table = input("Введіть назву таблиці: ")
                id = int(input("Введіть ID рядка, який потрібно видалити: "))
                return table, id
            except ValueError as e:
                print(f"Помилка: {e}")

    def generate_data_input(self):
        while True:
            try:
                table_name = input("Введіть назву таблиці: ")
                rows_count = int(input("Введіть кількість рядків для генерації: "))
                return table_name, rows_count
            except ValueError as e:
                print(f"Помилка: {e}")

    def get_training_first_input(self):
        while True:
            try:
                user_weight = int(input("Введіть вагу користувача: "))
                exercise_name = input("Введіть назву вправи: ")
                return user_weight, exercise_name
            except ValueError as e:
                print(f"Помилка: {e}")

    def get_exercise_name_input(self):
        while True:
            try:
                number_of_sets = int(input("Введіть точну кількість підходів: "))
                difficulty = int(input("Введіть точний рівень складності вправи: "))
                return number_of_sets, difficulty
            except ValueError as e:
                print(f"Помилка: {e}")

    def get_avg_exercises_input(self):
        while True:
            try:
                date = input("Введіть дату: ")
                return date
            except ValueError as e:
                print(f"Помилка: {e}")

