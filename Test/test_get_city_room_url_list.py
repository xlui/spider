import json
import unittest
from random import seed, randint
from Config.config import city_json_file
from App.get_city_room_url_list import GetCityRoomUrlList


def random_url():
    with open(city_json_file, 'r', encoding='utf-8') as f:
        cities = json.load(f)
    return cities[randint(0, len(cities) - 1)].get('url')


class MyTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        from time import time
        seed(time())
        self.api = GetCityRoomUrlList(random_url())

    def test_get_urls(self):
        urls = self.api.get(3)
        self.assertTrue(urls)
        self.assertGreater(len(urls), 0)

    def test_again(self):
        urls = self.api.get(2)
        self.assertFalse(not urls)


if __name__ == '__main__':
    unittest.main()
