from src.shared.database.interfaces.DBDriver import DBDriver
from src.main.base.Player import Player

class PlayerModel:
    def __init__(self, driver: DBDriver):
        self.driver = driver

    def get_player_by_nick(self, nick: str):
        query = "SELECT * FROM player WHERE nick = %s"
        params = (nick,)
        return self.driver.select(query, params)

    def get_player_by_name(self, name: str):
        query = "SELECT * FROM player WHERE name = %s"
        params = (name,)
        return self.driver.select(query, params)

    def get_player_by_id(self, id: int):
        query = "SELECT * FROM player WHERE id = %s"
        params = (id,)
        return self.driver.select(query, params)

    def get_all(self):
        query = "SELECT * FROM player"
        return self.driver.select_all(query)

    def save(self, player: Player):
        query = "INSERT INTO player (name, nick) VALUES (%s, %s)"
        params = (player.name, player.nick)
        return self.driver.insert(query, params)

    def update(self, player: Player):
        query = "UPDATE player SET name = %s, nick = %s WHERE id = %s"
        params = (player.name, player.nick, player.id)
        return self.driver.update(query, params)

    def delete(self, id: int):
        query = "DELETE FROM player WHERE id = %s"
        params = (id,)
        return self.driver.delete(query, params)
