from src.shared.database.MySqlDriver import MySqlDriver
from src.shared.database.MySqlConnection import MySqlConnection
from ..model.PlayerModel import PlayerModel
from ..mapper.PlayerMapper import PlayerMapper

class PlayerService:
    def __init__(self):
        self.driver = MySqlDriver(MySqlConnection())
        self.model = PlayerModel(self.driver)

    def get_player_by_nick(self, nick: str):
        result = self.model.get_player_by_nick(nick)
        return PlayerMapper.from_touple(result)

    def save(self, player):
        return self.model.save(player)