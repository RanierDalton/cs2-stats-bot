from src.main.service.StatService import StatService
import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock dependencies
mock_mysql = MagicMock()
sys.modules['mysql'] = mock_mysql
sys.modules['mysql.connector'] = mock_mysql
sys.modules['dotenv'] = MagicMock()


class TestStatService(unittest.TestCase):

    @patch('src.main.service.StatService.StatModel')
    @patch('src.main.service.StatService.MySqlDriver')
    @patch('src.main.service.StatService.MySqlConnection')
    def setUp(self, mock_conn, mock_driver, mock_model_class):
        self.mock_model = mock_model_class.return_value
        self.service = StatService()

    def test_delete_stats_by_game_id(self):
        self.service.delete_stats_by_game_id(1)
        self.mock_model.delete_stats_by_game_id.assert_called_once_with(1)

    def test_get_player_stats_found(self):
        self.mock_model.get_player_stats.return_value = (
            "Ranie", 100, 50, 25, 2.5, 60.0, 40, 5000, 10
        )

        result = self.service.get_player_stats("ranie")

        self.assertIsNotNone(result)
        self.assertEqual(result['nick'], "Ranie")
        self.assertEqual(result['kills'], 100)
        self.assertEqual(result['kda'], 2.5)

    def test_get_player_stats_not_found(self):
        self.mock_model.get_player_stats.return_value = None
        result = self.service.get_player_stats("unknown")
        self.assertIsNone(result)

    def test_get_map_stats(self):
        # Model returns tuple with 10 columns
        # name, games, wins, loses, draws, avg_win, avg_lose, win_rate, avg_dmg, avg_hs
        self.mock_model.get_map_stats.return_value = (
            "Mirage", 10, 5, 5, 0, 13.0, 11.0, 50.0, 120.5, 35.0
        )

        result = self.service.get_map_stats("Mirage")

        self.assertIsNotNone(result)
        self.assertEqual(result['name'], "Mirage")
        self.assertEqual(result['win_rate'], 50.0)
        self.assertEqual(result['avg_damage'], 120.5)
        self.assertEqual(result['avg_headshot'], 35.0)

    def test_get_all_maps_stats(self):
        # name, games, wins, loses, draws, avg_win, avg_lose, win_rate
        self.mock_model.get_all_maps_stats.return_value = [
            ("Mirage", 10, 5, 5, 0, 13.0, 11.0, 50.0),
            ("Nuke", 5, 2, 3, 0, 10.0, 13.0, 40.0)
        ]

        stats = self.service.get_all_maps_stats()

        self.assertEqual(len(stats), 2)
        self.assertEqual(stats[0]['name'], "Mirage")
        self.assertEqual(stats[0]['win_rate'], 50.0)
        self.assertEqual(stats[1]['name'], "Nuke")

    def test_get_all_maps_stats_sort(self):
        self.mock_model.get_all_maps_stats.return_value = []
        self.service.get_all_maps_stats(sort_by="win_rate")
        self.mock_model.get_all_maps_stats.assert_called_with("win_rate")


if __name__ == '__main__':
    unittest.main()
