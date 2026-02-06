import mysql.connector as mysql
from .interfaces.DBConnection import DBConnection
import os
from dotenv import load_dotenv
load_dotenv()


class MySqlConnection(DBConnection):
    def __init__(self):
        self._host = os.getenv("DB_HOST")
        self._port = os.getenv("DB_PORT", 3306)
        self._user = os.getenv("DB_USER")
        self._password = os.getenv("DB_PASSWORD")
        self._database = os.getenv("DB_NAME")
        self._connection = None
        self._cursor = None
        self.connect()

    def connect(self):
        if self._connection is None or not self._connection.is_connected():
            self._connection = mysql.connect(
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._password,
                database=self._database,
                charset='utf8mb4',
                use_unicode=True
            )
            self._cursor = self._connection.cursor()
            # Force UTF-8 for the connection
            self._cursor.execute("SET NAMES utf8mb4")
            self._cursor.execute("SET CHARACTER SET utf8mb4")
            self._cursor.execute("SET character_set_connection=utf8mb4")

    def disconnect(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
