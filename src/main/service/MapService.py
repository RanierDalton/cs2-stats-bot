from ..model.MapModel import MapModel
from src.shared.database.MySqlConnection import MySqlConnection
from src.shared.database.MySqlDriver import MySqlDriver
from src.main.base.Map import Map

class MapService:
    def __init__(self):
        driver = MySqlDriver(MySqlConnection())
        self.driver = driver
        self.model = MapModel(driver)

    def create(self, name: str, is_active: bool = True):
        existing_id = self.model.get_id_by_name(name)
        if existing_id:
            raise ValueError(f"Mapa com nome '{name}' já existe.")
        
        map = Map(None, name, is_active)
        return self.model.create(map)

    def get_id_by_name(self, name: str) -> int:
        return self.model.get_id_by_name(name)

    def get_all(self):
        results = self.model.get_all() 
        maps = []
        if not results:
            return maps
        for row in results:
             maps.append(Map(row[0], row[1], bool(row[2])))
        return maps

    def get_by_id(self, id: int):
        result = self.model.get_by_id(id) # Returns ONE tuple or None
        if result:
            row = result # Result IS the row
            return Map(row[0], row[1], bool(row[2]))
        return None

    def update(self, map: Map):
         # Validation: Check if new name conflicts (if name changed)
        existing_id = self.model.get_id_by_name(map.name)
        if existing_id and existing_id != map.id:
             raise ValueError(f"Já existe outro mapa com o nome '{map.name}'.")

        return self.model.update(map)

    def delete(self, id: int):
        return self.model.delete(id)