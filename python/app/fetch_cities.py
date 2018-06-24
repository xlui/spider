# coding:utf-8
# 获得提供租房信息的城市列表
import json
from random import randint

import requests
from bs4 import BeautifulSoup

from config.config import city_url, headers, headers_count, city_json_file


class Cities:
    """分析网站，找到了声明城市列表的 url，从中提取所有城市信息"""

    def __init__(self, root_url=city_url):
        super(Cities, self).__init__()
        self.__root_url = root_url

    def __get_cities(self):
        """获取城市列表的细节

        :return: 租房信息列表
        """
        city_list = []

        start_cities = ['var', 'citys=new', 'Array()']
        stop_cities = ['var', 'abroadcitys=new', 'Array()']
        start_abroad_cities = ['var', 'abroadcitys=new', 'Array()']
        stop_abroad_cities = ['abroadcitys[80]=new',
                              "Array('burnaby','本那比','burnaby','burnaby','1','','不列颠哥伦比亚省','','',2804,1,'-8:00')"]

        web_data = requests.get(self.__root_url,
                                headers=headers[randint(0, headers_count - 1)])
        web_data.encoding = 'utf-8'
        lines = [data.split() for data in web_data.text.split(';')]

        normal_cities = lines[lines.index(start_cities) + 1: lines.index(stop_cities)]
        abroad_cities = lines[lines.index(start_abroad_cities) + 1: lines.index(stop_abroad_cities) + 1]
        all_cities = normal_cities + abroad_cities
        # current data format:
        # all_cities[0] = ['citys[0]=new', "Array('bj','北京','beijing','bj','8673','beijing','北京','','',12,0)"]

        dealt_cities = [all_city[1].split(',') for all_city in all_cities]
        # current format:
        # dealt_cities[0] = ["Array('bj'", "'北京'", "'beijing'", "'bj'", "'8673'", "'beijing'", "'北京'", "''", "''", '12', '0)']
        # and we just need to care the second and the third column

        city_list = [
            {
                'city': eval(dealt_city[1]),
                'url': 'http://{}.xiaozhu.com'.format(eval(dealt_city[2])),
            } for dealt_city in dealt_cities
        ]

        print('Successfully fetch cities')
        return city_list

    def __get_pages(self):
        city_list = self.__get_cities()
        for city in city_list:
            # sleep(randint(20, 60))
            web_data = requests.get(city.get('url'),
                                    headers=headers[randint(0, headers_count - 1)])
            web_data.encoding = 'utf-8'
            soup = BeautifulSoup(web_data.text, 'lxml')
            total = soup.select('input#totalPages')
            if len(total) != 0:
                page = total[0].get('value')
                print('Successfully get total pages of [{}]'.format(city.get('city')))
            else:
                print('Failed to get total pages of [{}]'.format(city.get('city')))
                page = 0
            city['page'] = page
        return city_list

    def save(self, to_db=False):
        """将城市信息以JSON形式保存在：data/cities.json

        :return: none
        """
        city_list = self.__get_pages()  # type: list
        with open(city_json_file, 'w', encoding='utf-8') as file:
            print('Dump cities to file')
            json.dump(city_list, file)
        if to_db:
            from app.mysql import MySQL
            from contextlib import closing

            with closing(MySQL()) as db:
                db.execute('DROP TABLE IF EXISTS cities')
                db.execute('CREATE TABLE cities('
                           '  id INT AUTO_INCREMENT PRIMARY KEY,'
                           '  city_name CHAR(20),'
                           '  city_url VARCHAR(128),'
                           '  page INT'
                           ') ENGINE=INNODB CHAR SET=utf8')
                print('Writing data to database')
                [db.execute(
                    'INSERT INTO cities(city_name, city_url, page) VALUES ("{city_name}", "{city_url}", "{page}")'.format(
                        city_name=city.get('city'),
                        city_url=city.get('url'),
                        page=city.get('page'))) for city in city_list]

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
    fetch_cities = Cities()
    fetch_cities.save(True)
    cities = fetch_cities.get()
    for city in cities:
        print(city)
    print('Total: {}'.format(len(cities)))
