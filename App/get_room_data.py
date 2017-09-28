#!/usr/bin/env python
# coding: utf-8
# module to get detail data from room link
import requests
from bs4 import BeautifulSoup
from random import randint
from Config.config import headers, headers_length, proxies, proxies_length


class GetRoomData(object):
    """Class GetRoomData: get DETAILED data of the room from the room link"""
    def __init__(self, url):
        super(GetRoomData, self).__init__()
        self.__url = url
        self.__data = {}

    def __get_data(self):
        """From room link get DETAILED data, also solve exceptions

        :return: room data dict
        """
        web_data = requests.get(self.__url,
                                headers=headers[randint(0, headers_length)],
                                proxies=proxies[randint(0, proxies_length)])
        web_data.encoding = 'utf-8'
        soup = BeautifulSoup(web_data.text, 'lxml')

        # todo: find a better way to do this.
        t_title = soup.select('h4 em')
        title = None if not t_title else t_title[0].text

        t_address = soup.select('span.pr5')
        address = None if not t_address else t_address[0].text

        t_price = soup.select('div.day_l span')
        price = None if not t_price else t_price[0].text

        t_img = soup.select('#curBigImage')
        img = None if not t_img else t_img[0].get('src')

        t_host_pic = soup.select('div.member_pic a img')
        host_pic = None if not t_host_pic else t_host_pic[0].get('src')

        t_host_name = soup.select('h6 a.lorder_name')
        host_name = None if not t_host_name else t_host_name[0].text

        host_gender = 'female' if soup.find_all('.member_ico1') else 'male'

        self.__data = {
            'title': title,
            'address': address,
            'price': price,
            'img': img,
            'host_pic': host_pic,
            'host_name': host_name,
            'host_gender': host_gender,
        }

        for key, value in self.__data.items():
            # get rid of spaces and '\n' at the last of value
            try:
                self.__data[key] = value.strip()
            except AttributeError:
                pass

        return self.__data

    def get(self):
        """Packaging the detail code of getting room data

        :return: room data list
        """
        return self.__get_data()

    def print(self):
        """Simply print out the data collected

        :return: none
        """
        self.__get_data()
        for key, value in self.__data.items():
            print(key, value)


if __name__ == '__main__':
    url = 'http://bj.xiaozhu.com/fangzi/14936062703.html'
    get_room_data = GetRoomData(url)
    print(get_room_data.get())
