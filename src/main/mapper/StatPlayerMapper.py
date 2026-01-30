from src.main.base.dto.StatPlayerDTO import StatPlayerDTO


class StatPlayerMapper:
    @staticmethod
    def from_touple_list(data):
        list = []
        for stat in data:
            list.append(StatPlayerMapper.from_touple(stat))
        return list

    @staticmethod
    def from_touple(data):
        player = StatPlayerDTO(
            nick=data[0],
            kda=f"{data[1]:.2f}",
            winrate=f"{data[2]:.2f}",
            best_map=data[3],
            worse_map=data[4]
        )
        return player
