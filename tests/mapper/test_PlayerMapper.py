import unittest
from src.main.mapper.PlayerMapper import PlayerMapper

class TestPlayerMapper(unittest.TestCase):

    def test_from_dict(self):
        data = {'name': 'Ranie', 'nick': 'ranie'}
        player = PlayerMapper.from_dict(data, game_id=1)
        self.assertEqual(player.name, 'Ranie')
        self.assertEqual(player.nick, 'ranie')
        self.assertEqual(player.game_id, 1)

    def test_from_touple(self):
        data = (10, 'Lucas', 'lucas_nick')
        player = PlayerMapper.from_touple(data)
        self.assertEqual(player.id, 10)
        self.assertEqual(player.name, 'Lucas')
        self.assertEqual(player.nick, 'lucas_nick')

if __name__ == '__main__':
    unittest.main()
