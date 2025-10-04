from src.shared.database.MySqlConnection import MySqlConnection
from src.shared.database.MySqlDriver import MySqlDriver
from src.main.model.GameModel import GameModel
from src.main.base.Game import Game

class GameService:
    def __init__(self):
        driver = MySqlDriver(MySqlConnection())
        self.driver = driver
        self.model = GameModel(driver)

    def save_game(self, game: Game) -> int:
        return self.model.create(game)

