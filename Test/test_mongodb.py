from random import randint
import unittest
from App.mongodb import MongoDB


class MyTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.mongodb = MongoDB()
        self.collection = 'test'

    def tearDown(self):
        super().tearDown()
        self.mongodb.close()

    def test_drop(self):
        collections = [chr(i) for i in range(97, 97+26)]
        self.assertFalse(self.mongodb.drop(collections[randint(0, 26)]))

        self.mongodb.save(collection=self.collection, test_name='test', test_url='https://www.test.com')
        self.assertTrue(self.mongodb.drop(self.collection))

    def test_save(self):
        self.assertTrue(self.mongodb.save(collection=self.collection, test_name='test', test_url='www.test.com'))
        self.assertFalse(not self.mongodb.drop(self.collection))


if __name__ == '__main__':
    unittest.main()
