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
    
    def get_all_players_stats(self):
        query = """
        SELECT
            PCS.nick,
            PCS.kda_carreira,
            PCS.win_rate_medio,
            PMP_BEST.map_name AS melhor_mapa,
            PMP_WORST.map_name AS pior_mapa
        FROM
            -- Player Career Stats (PCS) as a Subquery
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
            -- Best Map Performance (PMP_BEST) using an outer Subquery
            (
                SELECT
                    player_id,
                    map_name,
                    kda_mapa,
                    win_rate_mapa
                FROM
                    -- Nested Subquery for Map Ranking (Requires MySQL 8.0+ for ROW_NUMBER())
                    (
                        SELECT
                            P.id AS player_id,
                            M.name AS map_name,
                            (SUM(GD.kills) + SUM(GD.assists)) / NULLIF(SUM(GD.deaths), 0) AS kda_mapa,
                            AVG(CASE WHEN G.status = 'win' THEN 100.0 ELSE 0.0 END) AS win_rate_mapa,
                            
                            -- !!! ATTENTION: This ROW_NUMBER() function still requires MySQL 8.0+ !!!
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
            -- Worst Map Performance (PMP_WORST) using an outer Subquery
            (
                SELECT
                    player_id,
                    map_name,
                    kda_mapa,
                    win_rate_mapa
                FROM
                    -- Nested Subquery for Map Ranking (Requires MySQL 8.0+ for ROW_NUMBER())
                    (
                        SELECT
                            P.id AS player_id,
                            M.name AS map_name,
                            (SUM(GD.kills) + SUM(GD.assists)) / NULLIF(SUM(GD.deaths), 0) AS kda_mapa,
                            AVG(CASE WHEN G.status = 'win' THEN 100.0 ELSE 0.0 END) AS win_rate_mapa,
                            
                            -- !!! ATTENTION: This ROW_NUMBER() function still requires MySQL 8.0+ !!!
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