#!/usr/bin/env python
# coding: utf-8
# module to get detail data from room link
import requests
from time import sleep
from random import randint
from bs4 import BeautifulSoup
from random import randint
from Config.config import headers, headers_length, proxies, proxies_length


class GetRoomData(object):
    """Class GetRoomData: get DETAILED data of the room from the room link"""
    def __init__(self):
        super(GetRoomData, self).__init__()
        self.__data = {}

    def __get_data(self, url):
        # sleep(randint(0, 20))
        web_data = requests.get(url,
                                headers=headers[randint(0, headers_length - 1)],
                                proxies=proxies[randint(0, proxies_length - 1)])
        web_data.encoding = 'utf-8'
        soup = BeautifulSoup(web_data.text, 'lxml')

        tmp_json = {
            'title': soup.select('h4 em'),
            'address': soup.select('span.pr5'),
            'price': soup.select('div.day_l span'),
            'img': soup.select('#curBigImage'),
            'host_pic': soup.select('div.member_pic a img'),
            'host_name': soup.select('h6 a.lorder_name'),
            'host_gender': 'female' if soup.select('.member_ico1') else 'male'
        }

        self.__data = {
            'title': '' if not tmp_json['title'] else tmp_json['title'][0].text,
            'address': '' if not tmp_json['address'] else tmp_json['address'][0].text,
            'price': '' if not tmp_json['price'] else tmp_json['price'][0].text,
            'img': '' if not tmp_json['img'] else tmp_json['img'][0].get('src', ''),
            'host_pic': '' if not tmp_json['host_pic'] else tmp_json['host_pic'][0].get('src', ''),
            'host_name': '' if not tmp_json['host_name'] else tmp_json['host_name'][0].text,
            'host_gender': tmp_json['host_gender'],
        }

        self.__data = {key: value.strip() for key, value in self.__data.items()}

        print('{} get data from room url.'.format('Successfully' if self.__data else 'Failed to'))
        return self.__data

    def get(self, url):
        """From room link `url` get detail data

        :return: room data dict
        """
        return self.__get_data(url)

    def print(self, url):
        """Simply print out the data collected

        :return: none
        """
        self.__get_data(url)
        for key, value in self.__data.items():
            print(key, value)


if __name__ == '__main__':
    url = 'http://aomen.xiaozhu.com/fangzi/18984852103.html'
    get_room_data = GetRoomData()
    data = get_room_data.get(url)
    for key, value in data.items():
        print('{}: {}'.format(key, value))
