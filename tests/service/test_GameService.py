import unittest
from unittest.mock import MagicMock, patch
import sys

mock_mysql = MagicMock()
sys.modules['mysql'] = mock_mysql
sys.modules['mysql.connector'] = mock_mysql
sys.modules['dotenv'] = MagicMock()

from src.main.service.GameService import GameService


class TestGameService(unittest.TestCase):

    @patch('src.main.service.GameService.GameModel')
    @patch('src.main.service.GameService.MySqlDriver')
    @patch('src.main.service.GameService.MySqlConnection')
    @patch('src.main.service.GameService.StatService')
    def setUp(self, mock_stat_service_class, mock_conn, mock_driver, mock_model_class):
        self.mock_model = mock_model_class.return_value
        self.mock_stat_service = mock_stat_service_class.return_value
        self.service = GameService()

    def test_delete_game_cascade(self):
        game_id = 10
        self.mock_model.get_by_id.return_value = (game_id, '13-11', 'win', 1)

        self.service.delete_game(game_id)

        self.mock_stat_service.delete_stats_by_game_id.assert_called_once_with(game_id)
        self.mock_model.delete.assert_called_once_with(game_id)

    def test_save_game(self):
        game = MagicMock()
        self.mock_model.create.return_value = 123

        result = self.service.save_game(game)

        self.mock_model.create.assert_called_once_with(game)
        self.assertEqual(result, 123)


if __name__ == '__main__':
    unittest.main()
