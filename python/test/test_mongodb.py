import unittest
from random import randint
from App.mongodb import MongoDB


class MyTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.db = MongoDB()
        self.collection = 'test'

    def tearDown(self):
        super().tearDown()
        self.db.drop(self.collection)
        self.db.close()

    def test_1save(self):
        # make sure test save first, because test_2drop will use save method
        self.assertTrue(self.db.save(collection=self.collection,
                                     test_name='test 1', test_url='http://www.test1.com'))
        self.assertFalse(not self.db.save(collection=self.collection,
                                          test_name='test 2', test_url='http://www.test2.com'))
        self.assertTrue(self.db.save(collection=self.collection,
                                     test_name='test 3', test_url='http://www.test3.com'))
        self.assertFalse(not self.db.save(collection=self.collection,
                                          test_name='test 4', test_url='http://www.test4.com'))

    def test_2drop(self):
        collections = [chr(i) for i in range(97, 97+26)]
        self.assertFalse(self.db.drop(collections[randint(0, 26 - 1)]))
        # the letter named collections won't appear in DB, so return 0

        self.db.save(collection=self.collection, test_name='test', test_url='https://www.test.com')
        self.assertTrue(self.db.drop(self.collection))
        # this will drop the collection 'test' and return 0
        self.assertFalse(self.db.drop(self.collection))
        # collection 'test' is not exist, return 0

    def test_3query(self):
        self.db.save(self.collection, title='test title 1', content='https://www.test1.com')
        self.db.save(self.collection, title='test title 2', content='https://www.test2.com')

        self.assertTrue(self.db.query(self.collection))
        self.assertFalse(not self.db.query(self.collection, title='test title 1'))
        self.assertTrue(self.db.query(self.collection, title='test title 2'))
        self.assertFalse(not self.db.query(self.collection, content='https://www.test2.com'))
        self.assertTrue(self.db.query(self.collection, content='https://www.test1.com'))


if __name__ == '__main__':
    unittest.main()
