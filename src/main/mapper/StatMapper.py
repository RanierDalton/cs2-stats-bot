from ..base.Stat import Stat

class StatMapper:
    @staticmethod
    def from_dict(data, game_id: int):
        kills = 0
        deaths = 0
        assists = 0

        try:
            kda_str = data.get('kda', '0/0/0')
            parts = kda_str.replace('-', '/').split('/')
            
            if len(parts) > 0:
                kills = int(parts[0]) if parts[0].strip().isdigit() else 0
            if len(parts) > 1:
                deaths = int(parts[1]) if parts[1].strip().isdigit() else 0
            if len(parts) > 2:
                assists = int(parts[2]) if parts[2].strip().isdigit() else 0
                
        except ValueError:
            print(f"Erro ao fazer parse do KDA: {data.get('kda')}")
            pass

        stat = Stat(
            id=None,
            kills=kills,
            deaths=deaths,
            assists=assists,
            headshot=int(str(data.get('hs', '0')).replace('%', '')), # Ensure string for replace
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