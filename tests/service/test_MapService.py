import unittest
from unittest.mock import MagicMock, patch
import sys

mock_mysql = MagicMock()
sys.modules['mysql'] = mock_mysql
sys.modules['mysql.connector'] = mock_mysql
sys.modules['dotenv'] = MagicMock()

from src.main.base.Map import Map  # noqa: E402
from src.main.service.MapService import MapService  # noqa: E402


class TestMapService(unittest.TestCase):

    @patch('src.main.service.MapService.MapModel')
    @patch('src.main.service.MapService.MySqlDriver')
    @patch('src.main.service.MapService.MySqlConnection')
    def setUp(self, mock_conn, mock_driver, mock_model_class):
        self.mock_model = mock_model_class.return_value
        self.service = MapService()

    def test_create_map_success(self):
        self.mock_model.get_id_by_name.return_value = None
        self.mock_model.create.return_value = 1

        result = self.service.create("Dust2")

        self.mock_model.create.assert_called_once()
        self.assertEqual(result, 1)

    def test_create_map_duplicate(self):
        self.mock_model.get_id_by_name.return_value = 5

        with self.assertRaises(ValueError) as context:
            self.service.create("Dust2")

        self.assertTrue("já existe" in str(context.exception))
        self.mock_model.create.assert_not_called()

    def test_update_map_success_same_name(self):
        map_obj = Map(1, "Dust2")
        self.mock_model.get_id_by_name.return_value = 1

        self.service.update(map_obj)
        self.mock_model.update.assert_called_once()

    def test_update_map_conflict(self):
        map_obj = Map(1, "Dust2_Renamed")
        self.mock_model.get_id_by_name.return_value = 2

        with self.assertRaises(ValueError):
            self.service.update(map_obj)

    def test_get_all_maps(self):
        self.mock_model.get_all.return_value = [
            (1, "Mirage", 1),
            (2, "Nuke", 0)
        ]

        maps = self.service.get_all()

        self.assertEqual(len(maps), 2)
        self.assertEqual(maps[0].name, "Mirage")
        self.assertTrue(maps[0].is_active)
        self.assertEqual(maps[1].name, "Nuke")
        self.assertFalse(maps[1].is_active)

    def test_search_maps(self):
        self.mock_model.search_by_name.return_value = [
            ("Dust2",),
            ("Mirage",)
        ]

        result = self.service.search_maps("")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "Dust2")
        self.assertEqual(result[1], "Mirage")


if __name__ == '__main__':
    unittest.main()
