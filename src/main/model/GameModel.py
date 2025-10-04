from src.shared.database.interfaces.DBDriver import DBDriver
from src.main.base.Game import Game

class GameModel:
    def __init__(self, driver: DBDriver):
        self.driver = driver

    def create(self, game: Game) -> int:
        query = """
        INSERT INTO game (dt, allies_rounds, adversary_rounds, fk_map, status)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (game.date, game.allies_rounds, game.adversary_rounds, game.map_id, game.status)
        return self.driver.insert(query, params)