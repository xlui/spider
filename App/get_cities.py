#!/usr/bin/env python
# coding:utf-8
# module to get cities that provided by www.xiaozhu.com which provide rental houses.
import json
import requests
from bs4 import BeautifulSoup
from random import randint
from Config.config import root_url, city_json_file, headers, headers_length, proxies, proxies_length


class GetCities(object):
    """Class GetCities: to get cities from http://www.xiaozhu.com"""
    def __init__(self):
        super(GetCities, self).__init__()
        self.__root_url = root_url

    def __get_cities(self):
        """Get city list from official website.

        :return: list of cities which provide rental room
        """
        web_data = requests.get(self.__root_url,
                                headers=headers[randint(0, headers_length - 1)],
                                proxies=proxies[randint(0, proxies_length - 1)])
        # headers is baidu spider header, to avoid being blocked.
        web_data.encoding = 'utf-8'
        soup = BeautifulSoup(web_data.text, 'lxml')
        label_a_list = soup.select('div.foot_v2 > dl.link_dl > dd > a')
        # get city list tags.
        # and because of the matching rule, the list will also contains ad links.

        city_list = []
        for index in range(len(label_a_list)):
            # print('type:', type(label_a_list[index]))
            # type: <class 'bs4.element.Tag'>
            url = label_a_list[index].get('href')
            # get url from Tag `a`.

            if 'xiaozhu' in url:
                # this blocks the ad url.
                city_name = label_a_list[index].text

                city_list.append({
                    'name': city_name,
                    'url': url
                })
        # return a list of dicts
        return city_list

    def save(self):
        """Save city data in JSON format to Config/cities.json

        :return: none
        """
        city_list = self.__get_cities()
        with open(city_json_file, 'w', encoding='utf-8') as file:
            json.dump(city_list, file)

    def get(self):
        """get JSON format data from Config/cities.json. If get None, request those data from the official website.

        :return: city url data list
        """
        with open(city_json_file, 'r', encoding='utf-8') as file:
            data_list = json.load(file)
        if data_list:
            return data_list
        else:
            return self.__get_cities()


if __name__ == '__main__':
    get_cities = GetCities()
    get_cities.save()
    cities = get_cities.get()
    for city in cities:
        print(city)
    print('Total: {}'.format(len(cities)))
