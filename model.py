import psycopg
import time

class Model:
    def __init__(self):
        self.conn = psycopg.connect(
            dbname='lab1',
            user='postgres',
            password='Vfdgjxrf1!',
            host='localhost',
            port=5432
        )

    def get_all_tables(self): # повертає усі таблиці в базі данних
        c = self.conn.cursor()
        c.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [table[0] for table in c.fetchall()]
        return tables

    def get_all_columns(self, table_name): # повертає усі колонки у відповідній таблиці
        c = self.conn.cursor()
        c.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position", (table_name,))
        columns = [row[0] for row in c.fetchall()]
        return columns

    def get_all_column_types(self, table_name, columns) -> dict: # повертає усі колонки і типи колонок у вигляді словника
        column_types = {}
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = %s AND column_name = ANY(%s);
            """, (table_name, columns))

            for column_name, data_type in cursor.fetchall():
                column_types[column_name] = data_type

        return column_types

    def get_foreign_keys(self, table): # повертає усі зовнішні ключі для відповідної таблиці
        query = f"""
            SELECT
                kcu.column_name,
                ccu.table_name AS referenced_table
            FROM
                information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
            WHERE tc.table_name = '{table}' AND tc.constraint_type = 'FOREIGN KEY';
        """
        c = self.conn.cursor()
        c.execute(query)
        foreign_keys = {row[0]: row[1] for row in c.fetchall()}
        return foreign_keys

    def add_data(self, table, columns, val): # додає дані до таблиці
        c = self.conn.cursor()
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(val))
        try:
            c.execute(f'INSERT INTO "public"."{table}" ({columns_str}) VALUES ({placeholders})', val)
            self.conn.commit()
            return "all done"
        except Exception as e:
            return e

    def read_data(self, table): # повертає дані з таблиці
        table_temp = table
        if table == 'users' or table == 'exercises':
            table_temp = table_temp[:-1]
        try:
            c = self.conn.cursor()
            c.execute(f'SELECT * FROM {table}')
            return c.fetchall()
        except Exception as e:
            print(e)

    def delete_data(self, table, id): # видаляє дані з таблиці
        table_temp = table
        if table == 'users' or table == 'exercises':
            table_temp = table_temp[:-1]
        try:
            c = self.conn.cursor()
            c.execute(f'DELETE FROM {table} WHERE {table_temp}_id = %s', (id,))
            self.conn.commit()
            return "all done"
        except Exception as e:
            return e

    def update_data(self, table, columns, id, new_values): # оновлює дані в таблиці
        if len(columns) > 1:
            columns_str = '=%s, '.join(columns).strip() + "=%s"
        else:
            columns_str = columns[0] + "=%s"
        table_temp = table
        if table == 'users' or table == 'exercises':
            table_temp = table_temp[:-1]
        try:
            c = self.conn.cursor()
            c.execute(f'UPDATE {table} SET {columns_str} WHERE {table_temp}_id=%s', (*new_values, id,))
            self.conn.commit()
            return "all done"
        except Exception as e:
            return e

    def generate_data(self, table, rows_count): # генерує і додає дані в таблицю
        try:
            c = self.conn.cursor()
            columns = self.get_all_columns(table)
            if table != "workout":
                del columns[0]
            columns_str = ', '.join(columns)
            column_types = self.get_all_column_types(table, columns)

            foreign_keys = self.get_foreign_keys(table)

            values_list = []
            for col in columns:
                if col in foreign_keys:
                    ref_table = foreign_keys[col]
                    table_temp = ref_table
                    if ref_table == 'users' or ref_table == 'exercises':
                        table_temp = table_temp[:-1]
                    c.execute(f"(SELECT {table_temp}_id FROM {ref_table} ORDER BY random() LIMIT 1)")
                    ref_value = c.fetchone()[0]  # Отримуємо перше значення з вибірки
                    values_list.append(str(ref_value))
                else:
                    if column_types[col] == 'integer':
                        values_list.append("(random() * 100)::INT")
                    elif column_types[col] == 'text':
                        values_list.append("array_to_string(array(select chr(65 + trunc(random() * 26)::int) from generate_series(1, 5)), '')")
                    elif column_types[col] == 'timestamp with time zone':
                        values_list.append("date_trunc('seconds', now() + (random() * INTERVAL '365 days' - INTERVAL '182 days'))")
                    else:
                        values_list.append("md5(random()::text)")

            values = ', '.join(values_list)

            sql = f"""
                DO $$
                DECLARE
                    record_count INT := {rows_count};
                BEGIN
                    FOR i IN 1..record_count LOOP
                        INSERT INTO {table} ({columns_str})
                        VALUES (
                            {values}
                        );
                    END LOOP;
                END $$;
                """
            c.execute(sql)
            self.conn.commit()
            return "all done"
        except Exception as e:
            return e

    def find_training_first(self, user_weight, exercise_name): # пошук тренування
        try:
            c = self.conn.cursor()
            sql = f"""
                SELECT DISTINCT t.training_id, t.start_date_time, t.end_date_time
                FROM training t
                JOIN users u ON t.user_id = u.user_id
                JOIN workout w ON t.training_id = w.training_id
                JOIN exercises e ON w.exercise_id = e.exercise_id
                WHERE u.user_weight = {user_weight}
                AND e.exercise_name = '{exercise_name}';
                """
            start_time = time.time()
            c.execute(sql)
            elapsed_time = time.time() - start_time
            res_time_string = f"Час виконання запиту: {elapsed_time:.4f} секунд"
            columns = []
            columns.append("training_id")
            columns.append("start_date_time")
            columns.append("end_date_time")
            return c.fetchall(), columns, res_time_string
        except Exception as e:
            print(e)
            return [], []

    def find_exercise_name(self, number_of_sets, difficulty): # пошук вправи
        try:
            c = self.conn.cursor()
            sql = f"""
                SELECT DISTINCT e.exercise_name, e.difficulty, w.number_of_sets FROM exercises e
                JOIN workout w ON e.exercise_id = w.exercise_id 
                WHERE w.number_of_sets = %s AND e.difficulty = %s;
                """

            columns = []
            columns.append("exercise_name")
            columns.append("difficulty")
            columns.append("number_of_sets")
            start_time = time.time()
            c.execute(sql, (number_of_sets, difficulty))
            elapsed_time = time.time() - start_time
            res_time_string = f"Час виконання запиту: {elapsed_time:.4f} секунд"
            return c.fetchall(), columns, res_time_string
        except Exception as e:
            print(e)
            return [], []

    def find_avg_exercises(self, date): # пошук середних показників для тренувань
        try:
            c = self.conn.cursor()
            sql = f"""
                SELECT 
                    t.start_date_time,
                    AVG(w.number_of_sets) AS avg_sets,
                    AVG(w.number_of_repetitions) AS avg_reps
                FROM 
                    training t
                JOIN 
                    workout w ON t.training_id = w.training_id
                WHERE        
                    t.start_date_time >= '{date}'
                GROUP BY 
                    t.start_date_time
                ORDER BY 
                    t.start_date_time DESC;
                """

            columns = []
            columns.append("exercise_name")
            columns.append("difficulty")
            columns.append("number_of_sets")
            start_time = time.time()
            c.execute(sql)
            elapsed_time = time.time() - start_time
            res_time_string = f"Час виконання запиту: {elapsed_time:.4f} секунд"
            return c.fetchall(), columns, res_time_string
        except Exception as e:
            print(e)
            return [], []