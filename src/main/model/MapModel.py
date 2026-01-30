from src.shared.database.interfaces.DBDriver import DBDriver
from src.main.base.Map import Map


class MapModel:
    def __init__(self, driver: DBDriver):
        self.driver = driver

    def create(self, map: Map):
        query = "INSERT INTO map (name, is_active) VALUES (%s, %s)"
        params = (map.name, 1 if map.is_active else 0)
        return self.driver.insert(query, params)

    def get_id_by_name(self, name: str):
        query = "SELECT id FROM map WHERE name = %s"
        params = (name,)
        result = self.driver.select(query, params)
        return result[0] if result else None

    def get_all(self):
        query = "SELECT * FROM map"
        return self.driver.select_all(query)

    def get_by_id(self, id: int):
        query = "SELECT * FROM map WHERE id = %s"
        params = (id,)
        return self.driver.select(query, params)

    def update(self, map: Map):
        query = "UPDATE map SET name = %s, is_active = %s WHERE id = %s"
        params = (map.name, 1 if map.is_active else 0, map.id)
        return self.driver.update(query, params)

    def delete(self, id: int):
        query = "DELETE FROM map WHERE id = %s"
        params = (id,)
        return self.driver.delete(query, params)
