from ..base.Stat import Stat
from ..model.StatModel import StatModel
from src.shared.database.MySqlDriver import MySqlDriver
from src.shared.database.MySqlConnection import MySqlConnection

class StatService:
    def __init__(self):
        self.driver = MySqlDriver(MySqlConnection())
        self.model = StatModel(self.driver)

    def save_stat(self, stat: Stat):
        return self.model.save_stat(stat)