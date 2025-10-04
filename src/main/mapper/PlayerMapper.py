from ..base.Player import Player

class PlayerMapper:
    @staticmethod
    def from_dict(data, game_id: int):
        player = Player(
            id=None,
            name=data.get('name'),
            nick=data.get('nick')
        )
        player.game_id = game_id
        return player

    @staticmethod
    def from_dict_list(data_list, game_id: int):
        players = []
        for data in data_list:
            player = PlayerMapper.from_dict(data, game_id)
            players.append(player)
        return players
    
    @staticmethod
    def from_touple(data):
        player = Player(
            id=data[0],
            name=data[1],
            nick=data[2]
        )
        return player