from ..model.MapModel import MapModel
from src.shared.database.MySqlConnection import MySqlConnection
from src.shared.database.MySqlDriver import MySqlDriver

class MapService:
    def __init__(self):
        driver = MySqlDriver(MySqlConnection())
        self.driver = driver
        self.model = MapModel(driver)

    def get_id_by_name(self, name: str) -> int:
        id = self.model.get_id_by_name(name)
        return id if id else None