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

    def delete_stats_by_game_id(self, game_id: int):
        query = "DELETE FROM game_data WHERE fk_game = %s"
        params = (game_id,)
        return self.driver.delete(query, params)

    def get_player_stats(self, nick: str):
        query = """
        SELECT
            P.nick,
            SUM(GD.kills) AS total_kills,
            SUM(GD.deaths) AS total_deaths,
            SUM(GD.assists) AS total_assists,
            (SUM(GD.kills) + SUM(GD.assists)) / NULLIF(SUM(GD.deaths), 0) AS kda,
            AVG(CASE WHEN G.status = 'win' THEN 100.0 ELSE 0.0 END) AS win_rate,
            SUM(GD.headshot) AS total_headshots,
            SUM(GD.damage) AS total_damage,
            COUNT(G.id) as games_played
        FROM player P
        JOIN game_data GD ON P.id = GD.fk_player
        JOIN game G ON GD.fk_game = G.id
        WHERE P.nick = %s
        GROUP BY P.id, P.nick
        """
        params = (nick,)
        return self.driver.select(query, params)

    def get_map_stats(self, map_name: str):
        query = """
        SELECT
            M.name,
            COUNT(DISTINCT G.id) as games_played,
            SUM(CASE WHEN G.status = 'win' THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN G.status = 'lose' THEN 1 ELSE 0 END) as losses,
            SUM(CASE WHEN G.status = 'draw' THEN 1 ELSE 0 END) as draws,
            AVG(G.allies_rounds) as avg_rounds_won,
            AVG(G.adversary_rounds) as avg_rounds_lost
        FROM map M
        JOIN game G ON M.id = G.fk_map
        WHERE M.name = %s
        GROUP BY M.id, M.name
        """
        params = (map_name,)
        return self.driver.select(query, params)

    def get_all_maps_stats(self):
        query = """
        SELECT
            M.name,
            COUNT(DISTINCT G.id) as games_played,
            SUM(CASE WHEN G.status = 'win' THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN G.status = 'lose' THEN 1 ELSE 0 END) as losses,
            SUM(CASE WHEN G.status = 'draw' THEN 1 ELSE 0 END) as draws,
            AVG(G.allies_rounds) as avg_rounds_won,
            AVG(G.adversary_rounds) as avg_rounds_lost
        FROM map M
        LEFT JOIN game G ON M.id = G.fk_map
        GROUP BY M.id, M.name
        ORDER BY games_played DESC
        """
        return self.driver.select_all(query)

    def get_all_players_stats(self):
        query = """
        SELECT
            PCS.nick,
            PCS.kda_carreira,
            PCS.win_rate_medio,
            COALESCE(PMP_BEST.map_name, 'N/A') AS melhor_mapa,
            COALESCE(PMP_WORST.map_name, 'N/A') AS pior_mapa
        FROM
            (
                SELECT
                    P.id AS player_id,
                    P.nick,
                    (SUM(GD.kills) + SUM(GD.assists)) / NULLIF(SUM(GD.deaths), 0) AS kda_carreira,
                    AVG(CASE WHEN G.status = 'win' THEN 100.0 ELSE 0.0 END) AS win_rate_medio
                FROM
                    player P
                JOIN game_data GD ON P.id = GD.fk_player
                JOIN game G ON GD.fk_game = G.id
                GROUP BY P.id, P.nick
            ) AS PCS
        LEFT JOIN
            (
                SELECT
                    player_id,
                    map_name
                FROM
                    (
                        SELECT
                            P.id AS player_id,
                            M.name AS map_name,
                            ROW_NUMBER() OVER (
                                PARTITION BY P.id
                                ORDER BY (SUM(GD.kills) + SUM(GD.assists)) / NULLIF(SUM(GD.deaths), 0) DESC
                            ) AS rank_melhor_mapa
                        FROM
                            player P
                        JOIN game_data GD ON P.id = GD.fk_player
                        JOIN game G ON GD.fk_game = G.id
                        JOIN map M ON G.fk_map = M.id
                        GROUP BY P.id, M.name
                    ) AS RankedMaps
                WHERE RankedMaps.rank_melhor_mapa = 1
            ) AS PMP_BEST ON PCS.player_id = PMP_BEST.player_id
        LEFT JOIN
            (
                SELECT
                    player_id,
                    map_name
                FROM
                    (
                        SELECT
                            P.id AS player_id,
                            M.name AS map_name,
                            ROW_NUMBER() OVER (
                                PARTITION BY P.id
                                ORDER BY (SUM(GD.kills) + SUM(GD.assists)) / NULLIF(SUM(GD.deaths), 0) ASC
                            ) AS rank_pior_mapa
                        FROM
                            player P
                        JOIN game_data GD ON P.id = GD.fk_player
                        JOIN game G ON GD.fk_game = G.id
                        JOIN map M ON G.fk_map = M.id
                        GROUP BY P.id, M.name
                    ) AS RankedMaps
                WHERE RankedMaps.rank_pior_mapa = 1
            ) AS PMP_WORST ON PCS.player_id = PMP_WORST.player_id
        ORDER BY
            PCS.kda_carreira DESC;
        """
        return self.driver.select_all(query, params=None)
