from src.main.base.Player import Player
from src.main.service.PlayerService import PlayerService
import unittest
from unittest.mock import MagicMock, patch
import sys

mock_mysql = MagicMock()
sys.modules['mysql'] = mock_mysql
sys.modules['mysql.connector'] = mock_mysql
sys.modules['dotenv'] = MagicMock()


class TestPlayerService(unittest.TestCase):

    @patch('src.main.service.PlayerService.PlayerModel')
    @patch('src.main.service.PlayerService.MySqlDriver')
    @patch('src.main.service.PlayerService.MySqlConnection')
    def setUp(self, mock_conn, mock_driver, mock_model_class):
        self.mock_model = mock_model_class.return_value
        self.service = PlayerService()

    def test_create_player(self):
        player = Player(None, "Ranie", "ranie")
        self.service.save(player)
        self.mock_model.save.assert_called_with(player)

    def test_get_player_by_nick_found(self):
        # Model returns tuple
        self.mock_model.get_player_by_nick.return_value = (1, "Ranie", "ranie")

        result = self.service.get_player_by_nick("ranie")

        self.assertIsNotNone(result)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, "Ranie")
        self.assertEqual(result.nick, "ranie")

    def test_get_player_by_nick_not_found(self):
        self.mock_model.get_player_by_nick.return_value = None

        result = self.service.get_player_by_nick("unknown")

        self.assertIsNone(result)

    def test_get_all_players(self):
        self.mock_model.get_all.return_value = [
            (1, "Ranie", "ranie"),
            (2, "Lucas", "lucas")
        ]

        players = self.service.get_all()

        self.assertEqual(len(players), 2)
        self.assertEqual(players[0].name, "Ranie")
        self.assertEqual(players[1].name, "Lucas")


if __name__ == '__main__':
    unittest.main()
