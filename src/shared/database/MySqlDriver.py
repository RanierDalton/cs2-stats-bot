from .interfaces.DBDriver import DBDriver
from .interfaces.DBConnection import DBConnection

class MySqlDriver(DBDriver):
    def __init__(self, connection: DBConnection):
        super().__init__(connection)

    def update(self, query, params=None):
        self._connection._cursor.execute(query, params)
        self.commit()

    def insert(self, query, params=None):
        self._connection._cursor.execute(query, params)
        self.commit()
        return self._connection._cursor.lastrowid
    
    def delete(self, query, params=None):
        self._connection._cursor.execute(query, params)
        self.commit()

    def select_all(self, query, params=None):
        self._connection._cursor.execute(query, params)
        return self._connection._cursor.fetchall()
    
    def select(self, query, params=None):
        self._connection._cursor.execute(query, params)
        return self._connection._cursor.fetchone()
    
    def commit(self):
        self._connection._connection.commit()

    @property
    def connection(self):
        return super().connection