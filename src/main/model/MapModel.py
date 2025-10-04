from src.shared.database.interfaces.DBDriver import DBDriver
from src.main.base.Map import Map

class MapModel:
    def __init__(self, driver: DBDriver):
        self.driver = driver
    
    def create(self, map: Map):
        query = """
        INSERT INTO map (name)
        VALUES (%s)
        """
        params = (map.name,)
        return self.driver.insert(query, params)
    
    def get_id_by_name(self, name: str):
        query = "SELECT id FROM map WHERE name = %s"
        params = (name,)
        result = self.driver.select(query, params)
        return result[0] if result else None