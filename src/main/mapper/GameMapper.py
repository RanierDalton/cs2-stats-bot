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
        score = data.get('score', '')

        # Validate score format
        if not score or '-' not in score:
            raise ValueError(f"Score inválido: '{score}'. Esperado formato 'X-Y' (ex: '13-10')")

        score_parts = score.split('-')

        if len(score_parts) != 2:
            raise ValueError(f"Score inválido: '{score}'. Esperado formato 'X-Y' (ex: '13-10')")

        allies_rounds = score_parts[0].strip()
        adversary_rounds = score_parts[1].strip()

        # Validate that both parts are numeric
        if not allies_rounds.isdigit() or not adversary_rounds.isdigit():
            raise ValueError(f"Score inválido: '{score}'. Rounds devem ser números inteiros.")

        status = 'win' if int(allies_rounds) > int(adversary_rounds) else 'draw' if int(
            allies_rounds) == int(adversary_rounds) else 'lose'

        game = Game(
            allies_rounds=allies_rounds,
            adversary_rounds=adversary_rounds,
            status=status,
            map_id=map_id
        )

        return game
