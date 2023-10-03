from model import Model
from view import View


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            choice = self.show_menu()
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_tasks()
            elif choice == '3':
                self.update_task()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                break

    def show_menu(self):
        self.view.show_message("\nMenu:")
        self.view.show_message("1. Add Task")
        self.view.show_message("2. View Tasks")
        self.view.show_message("3. Update Task")
        self.view.show_message("4. Delete Task")
        self.view.show_message("5. Quit")
        return input("Enter your choice: ")

    def add_task(self):
        title, description = self.view.get_task_input()
        self.model.add_task(title, description)
        self.view.show_message("Task added successfully!")

    def view_tasks(self):
        tasks = self.model.get_all_tasks()
        self.view.show_tasks(tasks)

    def update_task(self):
        task_id = self.view.get_task_id()
        title, description = self.view.get_task_input()
        self.model.update_task(task_id, title, description)
        self.view.show_message("Task updated successfully!")

    def delete_task(self):
        task_id = self.view.get_task_id()
        self.model.delete_task(task_id)
        self.view.show_message("Task deleted successfully!")
