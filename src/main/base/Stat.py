class Stat:
    def __init__(self, id, kills, deaths, assists, headshot, damage, tag, player_nick, fk_player: int, fk_game: int):
        self._id = id
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.headshot = headshot
        self.damage = damage
        self.tag = tag
        self.player_nick = player_nick
        self.fk_player = fk_player
        self.fk_game = fk_game
