import sqlite3


class DBManager:
    def __init__(self, connection):
        self._connection = connection
        self._cursor = self._connection.cursor()

    def create_table(self, query) -> bool:
        try:
            self._cursor.execute(
                query
            )
            self._connection.commit()
        except Exception as e:
            print(e)
            return False

        return True

    def close(self) -> bool:
        try:
            self._cursor.close()
            self._connection.close()
        except Exception as e:
            print(e)
            return False
        return True

    def insert(self, table, *args) -> bool:
        placeholders = ', '.join(['?'] * len(args))
        query = f'INSERT INTO {table} VALUES ({placeholders})'
        try:
            self._cursor.execute(query, args)
            self._connection.commit()
        except Exception as e:
            print(e)
        return True
