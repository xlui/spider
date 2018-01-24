# coding: utf-8
# 从租房链接中得到房子的具体信息
from random import randint
from time import sleep

import requests
from bs4 import BeautifulSoup

from Config.config import headers, headers_count


class RoomData(object):
    """从房子链接中获取房子的详细信息"""

    def __init__(self):
        super(RoomData, self).__init__()
        self.__data = {}

    def __get_data(self, url):
        sleep(randint(0, 20))
        web_data = requests.get(url,
                                headers=headers[randint(0, headers_count - 1)],
                                )
        web_data.encoding = 'utf-8'
        soup = BeautifulSoup(web_data.text, 'lxml')

        tmp_json = {
            'title': soup.select('h4 em'),
            'address': soup.select('span.pr5'),
            'price': soup.select('div.day_l span'),
            'img': soup.select('#curBigImage'),
            'host_pic': soup.select('div.member_pic a img'),
            'host_name': soup.select('h6 a.lorder_name'),
            'host_gender': '女' if soup.select('.member_ico1') else '男',
            'zhima_credit': soup.select('.zm_credit'),
        }

        self.__data = {
            'title': '' if not tmp_json['title'] else tmp_json['title'][0].text,
            'address': '' if not tmp_json['address'] else tmp_json['address'][0].text,
            'price': '' if not tmp_json['price'] else tmp_json['price'][0].text,
            'img': '' if not tmp_json['img'] else tmp_json['img'][0].get('src', ''),
            'host_pic': '' if not tmp_json['host_pic'] else tmp_json['host_pic'][0].get('src', ''),
            'host_name': '' if not tmp_json['host_name'] else tmp_json['host_name'][0].text,
            'host_gender': tmp_json['host_gender'],
            'zhima_credit': '' if not tmp_json['zhima_credit'] else tmp_json.get('zhima_credit')[0].text,
        }

        self.__data = {key: value.strip() for key, value in self.__data.items()}

        print('{} get data from room url.'.format('Successfully' if self.__data else 'Failed to'))
        return self.__data

    def get(self, url):
        """向外部展示的 API

        :return: 房间信息的字典
        """
        return self.__get_data(url)

    def print(self, url):
        """获取房子信息，并输出

        :return: none
        """
        self.__get_data(url)
        for key, value in self.__data.items():
            print(key, value)


if __name__ == '__main__':
    url = 'http://aomen.xiaozhu.com/fangzi/18984852103.html'
    room_data = RoomData()
    data = room_data.get(url)
    for key, value in data.items():
        print('{}: {}'.format(key, value))
