from src.shared.database.interfaces.DBDriver import DBDriver
from src.main.base.Player import Player
from src.main.mapper.PlayerMapper import PlayerMapper

class PlayerModel:
    def __init__(self, driver: DBDriver):
        self.driver = driver

    def get_player_by_nick(self, nick: str):
        query = "SELECT * FROM player WHERE nick = %s"
        params = (nick,)
        return self.driver.select(query, params)