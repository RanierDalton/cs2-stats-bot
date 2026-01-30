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

    def delete_stats_by_game_id(self, game_id: int):
        return self.model.delete_stats_by_game_id(game_id)

    def get_all_players_stats(self) -> list:
        players_stats = self.model.get_all_players_stats()
        return StatPlayerMapper.from_touple_list(players_stats)

    def get_player_stats(self, nick: str):
        result = self.model.get_player_stats(nick)
        if result:
            row = result
            if not row[0]:
                return None
            return {
                "nick": row[0],
                "kills": row[1],
                "deaths": row[2],
                "assists": row[3],
                "kda": float(row[4]) if row[4] else 0.0,
                "win_rate": float(row[5]) if row[5] else 0.0,
                "headshots": row[6],
                "damage": row[7],
                "games": row[8]
            }
        return None

    def get_map_stats(self, map_name: str):
        result = self.model.get_map_stats(map_name)
        if result:
            row = result  # Result IS the row
            if not row[0]:
                return None
            return {
                "name": row[0],
                "games": row[1],
                "wins": row[2],
                "losses": row[3],
                "draws": row[4],
                "avg_rounds_won": float(row[5]) if row[5] else 0.0,
                "avg_rounds_lost": float(row[6]) if row[6] else 0.0,
                "win_rate": float(row[7]) if row[7] else 0.0,
                "avg_damage": float(row[8]) if row[8] else 0.0,
                "avg_headshot": float(row[9]) if row[9] else 0.0
            }
        return None

    def get_all_maps_stats(self, sort_by: str = 'games'):
        results = self.model.get_all_maps_stats(sort_by)
        if not results:
            return []

        maps_stats = []
        for row in results:
            if row[0]:
                maps_stats.append({
                    "name": row[0],
                    "games": row[1],
                    "wins": row[2],
                    "losses": row[3],
                    "draws": row[4],
                    "avg_rounds_won": float(row[5]) if row[5] else 0.0,
                    "avg_rounds_lost": float(row[6]) if row[6] else 0.0,
                    "win_rate": float(row[7]) if row[7] else 0.0
                })
        return maps_stats
