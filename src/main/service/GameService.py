from src.shared.database.MySqlConnection import MySqlConnection
from src.shared.database.MySqlDriver import MySqlDriver
from src.main.model.GameModel import GameModel
from src.main.base.Game import Game
from src.main.service.StatService import StatService


class GameService:
    def __init__(self):
        driver = MySqlDriver(MySqlConnection())
        self.driver = driver
        self.model = GameModel(driver)
        self.stat_service = StatService()

    def save_game(self, game: Game) -> int:
        return self.model.create(game)

    def delete_game(self, id: int):
        self.stat_service.delete_stats_by_game_id(id)
        return self.model.delete(id)

    def get_game_by_id(self, id: int):
        return self.model.get_by_id(id)
