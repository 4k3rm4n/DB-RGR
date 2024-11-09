from model import Model
from view import View


class Controller:
    def __init__(self):
        self.view = View()
        self.model = Model()

    def run(self):
        while True:
            choice = self.view.show_menu()
            if choice == '1':
                self.view_tables()
            elif choice == '2':
                self.view_columns()
            elif choice == '3':
                self.add_data()
            elif choice == '4':
                self.update_data()
            elif choice == '5':
                self.delete_data()
            elif choice == '6':
                self.generate_data()
            elif choice == '7':
                self.read_data()
            elif choice == '8':
                self.find_training_first()
            elif choice == '9':
                self.find_exercise_name()
            elif choice == '10':
                self.find_avg_exercises()
            elif choice == '11':
                break

    def view_tables(self):
        tables = self.model.get_all_tables()
        self.view.show_tables(tables)

    def view_columns(self):
        table = self.view.ask_table()
        columns = self.model.get_all_columns(table)
        self.view.show_columns(columns)

    def add_data(self):
        table, columns, val = self.view.insert()
        massage = self.model.add_data(table, columns, val)
        self.view.show_message(massage)

    def read_data(self):
        table = self.view.ask_table()
        columns = self.model.get_all_columns(table)
        data = self.model.read_data(table)
        self.view.show_data(data, columns)

    def delete_data(self):
        table, id = self.view.delete()
        massage = self.model.delete_data(table, id)
        self.view.show_message(massage)

    def update_data(self):
        table, columns, id, new_values = self.view.update()
        massage = self.model.update_data(table, columns, id, new_values)
        self.view.show_message(massage)

    def generate_data(self):
        table, rows_count = self.view.generate_data_input()
        massage = self.model.generate_data(table, rows_count)
        self.view.show_message(massage)

    def find_training_first(self):
        user_weight, exercise_name = self.view.get_training_first_input()
        data, columns, res_time = self.model.find_training_first(user_weight, exercise_name)
        if len(data) != 0:
            self.view.show_data(data, columns)
            self.view.show_message(res_time)
        else:
            self.view.show_message("нічого не знайшлося(")

    def find_exercise_name(self):
        number_of_sets, difficulty = self.view.get_exercise_name_input()
        data, columns, res_time = self.model.find_exercise_name(number_of_sets, difficulty)
        if len(data) != 0:
            self.view.show_data(data, columns)
            self.view.show_message(res_time)
        else:
            self.view.show_message("нічого не знайшлося(")

    def find_avg_exercises(self):
        date = self.view.get_avg_exercises_input()
        data, columns, res_time = self.model.find_avg_exercises(date)
        if len(data) != 0:
            self.view.show_data(data, columns)
            self.view.show_message(res_time)
        else:
            self.view.show_message("нічого не знайшлося(")
