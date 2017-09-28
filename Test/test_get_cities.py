import os
import unittest
from App.get_cities import GetCities
from Config.config import city_json_file


class MyTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.get_cities = GetCities()

    def test_save(self):
        self.get_cities.save()
        self.assertTrue(os.path.exists(city_json_file))

    def test_get(self):
        self.assertTrue(self.get_cities.get())


if __name__ == '__main__':
    unittest.main()
