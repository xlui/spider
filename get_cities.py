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
        web_data = requests.get(self.__root_url, headers)
        web_data.encoding = 'utf-8'
        city_list = []
        soup = BeautifulSoup(web_data.text, 'lxml')
        label_a_list = soup.select('div.foot_v2 > dl.link_dl > dd > a')

        for index in range(len(label_a_list)):
            url = label_a_list[index].get('href')
            city_url = url if 'xiaozhu' in url else None

            if city_url:
                city_name = label_a_list[index].text

                self.__cities.append(city_url)
                city_list.append({
                    'name':city_name,
                    'city':city_url
                })
        return city_list

    def save(self):
        city_list = self.__get_cities()
        with open('conf/cities.json', 'w', encoding='utf-8') as file:
            json.dump(city_list, file)

    def read(self):
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
