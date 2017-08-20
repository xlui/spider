#!/usr/bin/env python
# coding: utf-8
# module to get detail data from room link
import requests
from bs4 import BeautifulSoup
from conf.config import headers


class GetRoomData(object):
    """
    Class GetRoomData: get DETAILED data of the room from a room link
    """
    def __init__(self, url):
        super(GetRoomData, self).__init__()
        self.__url = url
        self.__data = {}

    def __get_data(self):
        """From room link get DETAILED data, also solve exceptions

        :return: room data dict
        """
        web_data = requests.get(self.__url, headers)
        web_data.encoding = 'utf-8'
        soup = BeautifulSoup(web_data.text, 'lxml')

        # todo: find a better way to do this.
        try:
            title = soup.select('h4 em')[0].text
        except IndexError as e:
            print(e)
            title = None

        try:
            address = soup.select('span.pr5')[0].text
        except Exception as e:
            print(e)
            address = None

        try:
            price = soup.select('div.day_l span')[0].text
        except Exception as e:
            print(e)
            price = None

        try:
            img = soup.select('#curBigImage')[0].get('src')
        except Exception as e:
            print(e)
            img = None

        try:
            host_pic = soup.select('div.member_pic a img')[0].get('src')
        except Exception as e:
            print(e)
            host_pic = None

        try:
            host_name = soup.select('h6 a.lorder_name')[0].text
        except Exception as e:
            print(e)
            host_name = None

        try:
            host_gender = 'female' if soup.find_all('div', 'member_ico1') else 'male'
        except Exception as e:
            print(e)
            host_gender = None

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
                self.__data[key] = None

        return self.__data

    def get(self):
        """Packaging the detail of getting room data

        :return: room data list
        """
        self.__get_data()
        return self.__data

    def print_data(self):
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
    # get_room_data.print_data()
