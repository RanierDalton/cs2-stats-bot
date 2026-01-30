from ..base.Game import Game
class GameMapper:
    @staticmethod
    def to_dict(game):
        return {
            "id": game.id,
            "date": game.date,
            "allies_rounds": game.allies_rounds,
            "adversary_rounds": game.adversary_rounds,
            "map_id": game.map_id
        }
    
    @staticmethod
    def from_dict(data, map_id: int):
        allies_rounds = data.get('score').split('-')[0]
        adversary_rounds = data.get('score').split('-')[1]

        status = 'win' if int(allies_rounds) > int(adversary_rounds) else 'draw' if int(allies_rounds) == int(adversary_rounds) else 'lose'

        game = Game(
            allies_rounds=allies_rounds,
            adversary_rounds=adversary_rounds,
            status=status,
            map_id=map_id
        )

        return game