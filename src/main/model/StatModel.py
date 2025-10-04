from ...shared.database.interfaces.DBDriver import DBDriver
from ..base.Stat import Stat

class StatModel:
    def __init__(self, driver: DBDriver):
        self.driver = driver

    def save_stat(self, stat: Stat):
        query = """
        INSERT INTO game_data (fk_player, fk_game, kills, deaths, assists, headshot, damage, tag)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            stat.fk_player,
            stat.fk_game,
            stat.kills,
            stat.deaths,
            stat.assists,
            stat.headshot,
            stat.damage,
            stat.tag,
        )
        return self.driver.insert(query, params)