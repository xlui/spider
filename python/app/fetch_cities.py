# coding:utf-8
# 获得提供租房信息的城市列表
import json
from random import randint

import requests

from config.config import headers, headers_count, city_json_file


class Cities:
    """分析网站，找到了声明城市列表的 url，从中提取所有城市信息"""

    def __init__(self, root_url='http://jci.xiaozhustatic1.com/e17092601/xzjs?k=Front_Index&httphost=www.xiaozhu.com'):
        super(Cities, self).__init__()
        self.__root_url = root_url

    def __get_cities(self):
        """获取城市列表的细节

        :return: 租房信息列表
        """
        city_list = []

        start_city = ['var', 'citys=new', 'Array()']
        stop_city = ['var', 'abroadcitys=new', 'Array()']
        start_abroad_cities = ['var', 'abroadcitys=new', 'Array()']
        stop_abroad_cities = ['abroadcitys[80]=new',
                              "Array('burnaby','本那比','burnaby','burnaby','1','','不列颠哥伦比亚省','','',2804,1,'-8:00')"]

        web_data = requests.get(self.__root_url,
                                headers=headers[randint(0, headers_count - 1)])
        web_data.encoding = 'utf-8'
        lines = [data.split() for data in web_data.text.split(';')]

        cities = lines[lines.index(start_city) + 1: lines.index(stop_city)]
        abroad_cities = lines[lines.index(start_abroad_cities) + 1: lines.index(stop_abroad_cities) + 1]
        # now data format:
        # cities[0] = ['citys[0]=new', "Array('bj','北京','beijing','bj','8673','beijing','北京','','',12,0)"]

        dealt_array_cities = [cities[i][1].split(',') for i in range(len(cities))]
        dealt_array_abroad_cities = [abroad_cities[i][1].split(',') for i in range(len(abroad_cities))]
        # now format:
        # dealt_array_cities[0] = ["Array('bj'", "'北京'", "'beijing'", "'bj'", "'8673'", "'beijing'", "'北京'", "''", "''", '12', '0)']
        # and we just need to care the second and the third data

        city_list.extend(
            {
                'city': eval(array_city[1]),
                'url': 'http://{}.xiaozhu.com'.format(eval(array_city[2])),
            } for array_city in dealt_array_cities
        )
        city_list.extend(
            {
                'city': eval(array_abroad_city[1]),
                'url': 'http://{}.xiaozhu.com'.format(eval(array_abroad_city[2])),
            } for array_abroad_city in dealt_array_abroad_cities
        )

        print('Successfully get cities')
        return city_list

    def save(self, to_db=False):
        """将城市信息以JSON形式保存在：Data/cities.json

        :return: none
        """
        city_list = self.__get_cities()  # type: list
        with open(city_json_file, 'w', encoding='utf-8') as file:
            print('Dump cities to file')
            json.dump(city_list, file)
        if to_db:
            from App.mysql import MySQL
            from contextlib import closing

            with closing(MySQL()) as db:
                db.execute('DROP TABLE IF EXISTS cities')
                db.execute(
                    'CREATE TABLE cities(id INT PRIMARY KEY AUTO_INCREMENT, city_name CHAR(10), url VARCHAR(32))')
                print('Writing data to database')
                [db.execute('INSERT INTO cities(city_name, url) VALUES ("{city_name}", "{url}")'.format(
                    city_name=city.get('city'),
                    url=city.get('url'))) for city in city_list]

    def get(self):
        """尝试从 Data/cities.json 中读取城市信息，如果读取失败，尝试从网站获取

        :return: city list
        """
        with open(city_json_file, 'r', encoding='utf-8') as file:
            data_list = json.load(file)
        if data_list:
            print('Successfully get data from Data/cities.json')
            return data_list
        else:
            print('Failed to get data from Data/cities.json, try to get through url')
            return self.__get_cities()


if __name__ == '__main__':
    get_cities = Cities()
    get_cities.save(to_db=True)
    cities = get_cities.get()
    for city in cities:
        print(city)
    print('Total: {}'.format(len(cities)))
