import os
import unittest
from App.fetch_cities import Cities
from Config.config import city_json_file, db_url, db_port, database, city_info_collection


class MyTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.get_cities = Cities()

    def test_save(self):
        self.get_cities.save()
        self.assertTrue(os.path.exists(city_json_file))

    def test_save_to_db(self):
        import pymongo
        db = pymongo.MongoClient(db_url, db_port)[database]
        db.drop_collection(city_info_collection)
        self.get_cities.save(to_db=True)
        self.assertGreater(db[city_info_collection].find().count(), 0)

    def test_get(self):
        self.assertTrue(self.get_cities.get())
        self.assertGreater(len(self.get_cities.get()), 0)


if __name__ == '__main__':
    unittest.main()
