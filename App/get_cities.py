#!/usr/bin/env python
# coding:utf-8
# module to get cities that provided by www.xiaozhu.com which provide rental houses.
import json
import requests
from random import randint
from Config.config import city_json_file, headers, headers_length, proxies, proxies_length


class GetCities(object):
    """Class GetCities: to get cities from a script link"""
    def __init__(self, root_url='http://jci.xiaozhustatic1.com/e17092601/xzjs?k=Front_Index&httphost=www.xiaozhu.com'):
        super(GetCities, self).__init__()
        self.__root_url = root_url

    def __get_cities(self):
        """Get city list from official website.

        :return: list of cities which provide rental room
        """
        city_list = []

        str_start_city = ['var', 'citys=new', 'Array()']
        str_stop_city = ['var', 'abroadcitys=new', 'Array()']
        str_start_abroad_cities = ['var', 'abroadcitys=new', 'Array()']
        str_stop_abroad_cities = ['abroadcitys[50]=new', "Array('huaxin','华欣','huaxin','huaxin','4','prachuap','班武里府','','',2741,1,'+7:00')"]

        web_data = requests.get(self.__root_url,
                                headers=headers[randint(0, headers_length - 1)],
                                proxies=proxies[randint(0, proxies_length - 1)])
        # headers is baidu spider header, to avoid being blocked.
        web_data.encoding = 'utf-8'
        dealt_texts = web_data.text.split(';')
        lines = [dealt_text.split() for dealt_text in dealt_texts]

        str_cities = lines[lines.index(str_start_city) + 1: lines.index(str_stop_city)]
        str_broad_cities = lines[lines.index(str_start_abroad_cities) + 1: lines.index(str_stop_abroad_cities) + 1]
        # now data format:
        # str_cities[0] = ['citys[0]=new', "Array('bj','北京','beijing','bj','7839','beijing','北京','','',12,0)"]

        dealt_array_cities = [str_cities[i][1].split(',') for i in range(len(str_cities))]
        dealt_array_broad_cities = [str_broad_cities[i][1].split(',') for i in range(len(str_broad_cities))]
        # now format:
        # dealt_array_cities[0] = ["Array('bj'", "'北京'", "'beijing'", "'bj'", "'7839'",
        #                       "'beijing'", "'北京'", "''", "''", '12', '0)']
        # and we just need to care the second and the third data

        city_list.extend([{
            'name': eval(dealt_array_cities[i][1]),
            'url': 'http://{}.xiaozhu.com'.format(eval(dealt_array_cities[i][2])),
        } for i in range(len(dealt_array_cities))])
        city_list.extend([{
            'name': eval(dealt_array_broad_cities[i][1]),
            'url': 'http://{}.xiaozhu.com'.format(eval(dealt_array_broad_cities[i][2])),
        } for i in range(len(dealt_array_broad_cities))])

        return city_list

    def save(self, to_db=False):
        """Save city data in JSON format to Config/cities.json

        :return: none
        """
        city_list = self.__get_cities()
        with open(city_json_file, 'w', encoding='utf-8') as file:
            json.dump(city_list, file)
        if to_db:
            from App.mongodb import MongoDB
            from contextlib import closing
            from threading import Thread
            with closing(MongoDB()) as mongodb:
                collection = 'Cities'
                mongodb.drop(collection=collection)
                thread_count = 20
                total_count = len(city_list)
                separate = total_count // thread_count
                threads = []

                def save_to_db(from_, to_):
                    sub_list = city_list[from_: to_]
                    for item in sub_list:
                        mongodb.save(collection, **item)

                for index in range(thread_count):
                    if index == (thread_count - 1):
                        thread = Thread(target=save_to_db, args=(index * separate, total_count))
                    else:
                        thread = Thread(target=save_to_db, args=(index * separate, index * separate + separate))
                    thread.start()
                    threads.append(thread)
                [thread.join() for thread in threads]

                print('Successfully saved data into MongoDB')

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
    get_cities.save(to_db=True)
    cities = get_cities.get()
    for city in cities:
        print(city)
    print('Total: {}'.format(len(cities)))
