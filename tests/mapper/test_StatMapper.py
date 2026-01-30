import unittest
from src.main.mapper.StatMapper import StatMapper


class TestStatMapper(unittest.TestCase):

    def test_kda_parsing_valid(self):
        data = {
            'kda': '20/10/5',
            'hs': '50%',
            'damage': '100',
            'tag': 'Test',
            'nick': 'Player1'
        }
        stat = StatMapper.from_dict(data, game_id=1)
        self.assertEqual(stat.kills, 20)
        self.assertEqual(stat.deaths, 10)
        self.assertEqual(stat.assists, 5)

    def test_kda_parsing_valid_hyphen(self):
        data = {
            'kda': '20-10-5',
            'hs': '50%',
            'damage': '100',
            'tag': 'Test',
            'nick': 'Player1'
        }
        stat = StatMapper.from_dict(data, game_id=1)
        self.assertEqual(stat.kills, 20)
        self.assertEqual(stat.deaths, 10)
        self.assertEqual(stat.assists, 5)

    def test_kda_parsing_partial(self):
        data = {
            'kda': '20/10',
            'hs': '50%',
            'damage': '100',
            'tag': 'Test',
            'nick': 'Player1'
        }
        stat = StatMapper.from_dict(data, game_id=1)
        self.assertEqual(stat.kills, 20)
        self.assertEqual(stat.deaths, 10)
        self.assertEqual(stat.assists, 0)  # Assumed 0

    def test_kda_parsing_single(self):
        data = {
            'kda': '20',
            'hs': '50%',
            'damage': '100',
            'tag': 'Test',
            'nick': 'Player1'
        }
        stat = StatMapper.from_dict(data, game_id=1)
        self.assertEqual(stat.kills, 20)
        self.assertEqual(stat.deaths, 0)
        self.assertEqual(stat.assists, 0)

    def test_kda_parsing_invalid(self):
        data = {
            'kda': 'invalid',
            'hs': '50%',
            'damage': '100',
            'tag': 'Test',
            'nick': 'Player1'
        }
        # Should NOT raise exception, but return 0s
        stat = StatMapper.from_dict(data, game_id=1)
        self.assertEqual(stat.kills, 0)
        self.assertEqual(stat.deaths, 0)
        self.assertEqual(stat.assists, 0)


if __name__ == '__main__':
    unittest.main()
