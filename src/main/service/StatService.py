from ..base.Stat import Stat
from ..model.StatModel import StatModel
from src.shared.database.MySqlDriver import MySqlDriver
from src.shared.database.MySqlConnection import MySqlConnection
from src.main.mapper.StatPlayerMapper import StatPlayerMapper

class StatService:
    def __init__(self):
        self.driver = MySqlDriver(MySqlConnection())
        self.model = StatModel(self.driver)

    def save_stat(self, stat: Stat) -> int:
        return self.model.save_stat(stat)
    
    def get_all_players_stats(self) -> list:
        players_stats = self.model.get_all_players_stats()
        print(players_stats)
        return StatPlayerMapper.from_touple_list(players_stats)