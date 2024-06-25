import sqlite3


class DBManager:
    def __init__(self, connection):
        self._connection = connection
        self._cursor = self._connection.cursor()

    def create_table(self) -> bool:
        if not self._cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                date TIMESTAMP,
                operation REAL,
                description TEXT
                )
                '''):
            return False
        self._connection.commit()
        return True

    def close(self):
        self._cursor.close()
        self._connection.close()

    def insert(self, *args):
        if self.create_table():
            print(args)
            self._cursor.execute('INSERT INTO users (id, date, operation, description) VALUES (?, ?, ?, ?)',
                                 (args[0], args[1], args[2], args[3]))
            self._connection.commit()
