from src.shared.database.MySqlDriver import MySqlDriver
from src.shared.database.MySqlConnection import MySqlConnection
from src.main.model.PlayerModel import PlayerModel
from src.main.mapper.PlayerMapper import PlayerMapper


class PlayerService:
    def __init__(self):
        self.driver = MySqlDriver(MySqlConnection())
        self.model = PlayerModel(self.driver)

    def get_player_by_nick(self, nick: str):
        result = self.model.get_player_by_nick(nick)
        if result:
            return PlayerMapper.from_touple(result)
        return None

    def get_player_by_name(self, name: str):
        result = self.model.get_player_by_name(name)
        if result:
            return PlayerMapper.from_touple(result)
        return None

    def get_player_by_id(self, id: int):
        result = self.model.get_player_by_id(id)
        if result:
            return PlayerMapper.from_touple(result)
        return None

    def get_all(self):
        results = self.model.get_all()
        if not results:
            return []
        return [PlayerMapper.from_touple(row) for row in results]

    def save(self, player):
        return self.model.save(player)

    def update(self, player):
        return self.model.update(player)

    def delete(self, id: int):
        return self.model.delete(id)
