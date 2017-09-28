import unittest
from random import randint
from App.get_room_data import GetRoomData


class MyTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.urls = [
            'http://bj.xiaozhu.com/fangzi/14936062703.html',
            'http://bj.xiaozhu.com/fangzi/2294529045.html',
            'http://bj.xiaozhu.com/fangzi/19497510303.html',
            'http://bj.xiaozhu.com/fangzi/10290768160.html',
            'http://bj.xiaozhu.com/fangzi/1956386571.html',
        ]
        self.getRoomData = GetRoomData(self.urls[randint(0, 5)])

    def test_get(self):
        self.assertTrue(self.getRoomData.get())


if __name__ == '__main__':
    unittest.main()
