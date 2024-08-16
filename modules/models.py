import sqlite3

class Core:
    def __init__(self):
        self.db_path = 'db.sqlite3'

    def _get_connection(self):
        # Create a new connection for the current thread
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        return connection, cursor

    def close(self, connection):
        connection.close()

class Numbers(Core):
    def __init__(self):
        super().__init__()
        self.__create_numbers_table()

    def __create_numbers_table(self):
        connection, cursor = self._get_connection()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS numbers(
                id INTEGER PRIMARY KEY,
                number TEXT NOT NULL UNIQUE
            )
        ''')
        connection.commit()
        self.close(connection)

    def add_number(self, number):
        try:
            connection, cursor = self._get_connection()
            number = str(number)
            cursor.execute('''INSERT INTO numbers(number) VALUES(?)''', (number,))
            connection.commit()
        except Exception as e:
            print(e)
        finally:
            self.close(connection)

    def read_numbers(self):
        connection, cursor = self._get_connection()
        cursor.execute('''SELECT * FROM numbers''')
        rows = cursor.fetchall()
        self.close(connection)
        return [row[1] for row in rows]

    def get_operation_by_number(self, number):
        connection, cursor = self._get_connection()
        number = str(number)
        cursor.execute('''SELECT number FROM numbers WHERE number = ?''', (number,))
        result = cursor.fetchone()
        self.close(connection)
        return result[0] if result else None

class File(Core):
    def __init__(self):
        super().__init__()
        self.__create_file_table()

    def __create_file_table(self):
        connection, cursor = self._get_connection()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file (
                name TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        connection.commit()
        self.close(connection)

    def add_file_info(self, file_name, created_at):
        connection, cursor = self._get_connection()
        cursor.execute('''INSERT INTO file(name, date) VALUES(?, ?)''', (file_name, created_at))
        connection.commit()
        self.close(connection)

    def get_last_record(self):
        connection, cursor = self._get_connection()
        cursor.execute('SELECT name, date FROM file ORDER BY date DESC LIMIT 1')
        record = cursor.fetchone()
        self.close(connection)
        return record
    
    def update_record(self, name, date):
        connection, cursor = self._get_connection()
        self.remove_file_info()
        cursor.execute('INSERT INTO file (name, date) VALUES (?, ?)', (name, date))
        connection.commit()
        self.close(connection)

    def remove_file_info(self):
        connection, cursor = self._get_connection()
        cursor.execute('''DELETE FROM file''')
        connection.commit()
        self.close(connection)