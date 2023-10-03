import psycopg2


class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='<YOUR PASSWORD>',
            host='localhost',
            port=5432
        )
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT
            )
        ''')

        # Check if the table exists
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tasks')")
        table_exists = c.fetchone()[0]

        if not table_exists:
            # Table does not exist, so create it
            c.execute('''
                CREATE TABLE tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT
                )
            ''')

        self.conn.commit()

    def add_task(self, title, description):
        c = self.conn.cursor()
        c.execute('INSERT INTO tasks (title, description) VALUES (%s, %s)', (title, description))
        self.conn.commit()

    def get_all_tasks(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM tasks')
        return c.fetchall()

    def update_task(self, task_id, title, description):
        c = self.conn.cursor()
        c.execute('UPDATE tasks SET title=%s, description=%s WHERE id=%s', (title, description, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM tasks WHERE id=%s', (task_id,))
        self.conn.commit()
