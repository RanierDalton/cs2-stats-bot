from ..base.Stat import Stat

class StatMapper:
    @staticmethod
    def from_dict(data, game_id: int):
        stat = Stat(
            id=None,
            kills=int(data.get('kda', '0').split('/')[0]),
            deaths=int(data.get('kda', '0').split('/')[1]),
            assists=int(data.get('kda', '0').split('/')[2]),
            headshot=int(data.get('hs', '0').replace('%', '')),
            damage=int(data.get('damage', '0')),
            tag=data.get('tag', ''),
            player_nick=data.get('nick', ''),
            fk_player=None,
            fk_game=game_id
        )
        return stat

    @staticmethod
    def from_dict_list(data_list, game_id: int):
        stats = []
        for data in data_list:
            data['fk_game'] = game_id
            stat = StatMapper.from_dict(data, game_id)
            stats.append(stat)
        return stats