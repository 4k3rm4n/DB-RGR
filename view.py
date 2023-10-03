class View:
    def show_tasks(self, tasks):
        print("Tasks:")
        for task in tasks:
            print(f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}")

    def get_task_input(self):
        title = input("Enter task title: ")
        description = input("Enter task description: ")
        return title, description

    def get_task_id(self):
        return int(input("Enter task ID: "))

    def show_message(self, message):
        print(message)
