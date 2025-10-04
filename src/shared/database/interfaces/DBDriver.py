from abc import ABC, abstractmethod
from .DBConnection import DBConnection

class DBDriver(ABC):
    def __init__(self, connection: DBConnection):
        self._connection = connection

    @abstractmethod
    def update(self, query, params=None):
        pass

    @abstractmethod
    def insert(self, query, params=None):
        pass

    @abstractmethod
    def delete(self, query, params=None):
        pass

    @abstractmethod
    def select(self, query, params=None):
        pass

    @abstractmethod
    def select_all(self, query, params=None):
        pass

    @abstractmethod
    def commit(self):
        pass

    @property
    def connection(self):
        return self._connection.connection