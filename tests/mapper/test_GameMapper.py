import unittest
from src.main.mapper.GameMapper import GameMapper

class TestGameMapper(unittest.TestCase):

    def test_from_dict_win(self):
        data = {'score': '13-5'}
        game = GameMapper.from_dict(data, map_id=1)
        self.assertEqual(game.allies_rounds, '13')
        self.assertEqual(game.adversary_rounds, '5')
        self.assertEqual(game.status, 'win')

    def test_from_dict_loss(self):
        data = {'score': '5-13'}
        game = GameMapper.from_dict(data, map_id=1)
        self.assertEqual(game.allies_rounds, '5')
        self.assertEqual(game.adversary_rounds, '13')
        self.assertEqual(game.status, 'lose')

    def test_from_dict_draw(self):
        data = {'score': '15-15'}
        game = GameMapper.from_dict(data, map_id=1)
        self.assertEqual(game.allies_rounds, '15')
        self.assertEqual(game.adversary_rounds, '15')
        self.assertEqual(game.status, 'draw')

if __name__ == '__main__':
    unittest.main()
