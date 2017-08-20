#!/usr/bin/env python
# coding:utf-8
# module to get cities that provided by www.xiaozhu.com which provide rental housing.
import json
import requests
from bs4 import BeautifulSoup
from conf.config import root_url, headers


class GetCities(object):
    """
    Class GetCities: to get cities from www.xiaozhu.com
    """
    def __init__(self):
        super(GetCities, self).__init__()
        self.__root_url = root_url
        self.__cities = []

    def __get_cities(self):
        """
        Get city list from official website

        :return: list of cities which provide rental room
        """
        web_data = requests.get(self.__root_url, headers)
        # headers is baidu spider header, to avoid being blocked
        web_data.encoding = 'utf-8'
        soup = BeautifulSoup(web_data.text, 'lxml')
        label_a_list = soup.select('div.foot_v2 > dl.link_dl > dd > a')
        # get city list label and because of the matching rule, the list
        # will also contains ad links

        city_list = []
        for index in range(len(label_a_list)):
            # print('type:', type(label_a_list[index]))
            # type: <class 'bs4.element.Tag'>
            url = label_a_list[index].get('href')
            # get url from label
            city_url = url if 'xiaozhu' in url else None
            # block ad url

            if city_url:
                city_name = label_a_list[index].text

                self.__cities.append(city_url)
                city_list.append({
                    'name': city_name,
                    'city': city_url
                })
        # return a list of dicts
        return city_list

    def print_(self):
        """
        print city list
        :return: none
        """
        city_list = self.__get_cities()
        print('The cities: ')
        for city in city_list:
            print(city)
        print('Total: {}'.format(len(city_list)))

    def save(self):
        """
        Save city data in JSON format to conf/cities.json
        :return: none
        """
        city_list = self.__get_cities()
        with open('conf/cities.json', 'w', encoding='utf-8') as file:
            json.dump(city_list, file)

    @staticmethod
    def read():
        """
        Read JSON format data from conf/cities.json and print
        :return: none
        """
        with open('conf/cities.json', 'r', encoding='utf-8') as file:
            data_list = json.load(file)
        print('The cities: ')
        for data in data_list:
            print(data)
        print('Total: {}'.format(len(data_list)))

if __name__ == '__main__':
    get_cities = GetCities()
    get_cities.save()
    get_cities.read()
    # get_cities.print_()
