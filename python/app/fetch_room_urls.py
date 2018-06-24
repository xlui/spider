# coding:utf-8

from random import randint
from time import sleep
import json

import requests
from bs4 import BeautifulSoup

from config.config import headers, headers_count, url_json_file


class RoomUrls(object):
    """获取一个城市的所有出租房的 url，存入数据库"""

    def __init__(self, city_url):
        super(RoomUrls, self).__init__()
        self.__page_base_url = city_url + "/search-duanzufang-p{}-0/"
        self.proxies = {'https': 'https://124.231.64.180:3128'}

    def get(self, city, page=13):
        """获得一个城市中所有的房子链接

        :param city: 城市名
        :param page: 城市房子页数
        :return: 房子链接列表
        """
        room_url_list = []

        for index in range(page + 1):
            sleep(randint(20, 60))
            # avoid too frequently request
            print('Fetching the {index} page...'.format(index=index))
            page_url = self.__page_base_url.format(index)
            web_data = requests.get(page_url, headers=headers[randint(0, headers_count - 1)], proxies=self.proxies)
            web_data.encoding = 'utf-8'
            soup = BeautifulSoup(web_data.text, 'lxml')
            room_url_tags = soup.select('div.result_btm_con.lodgeunitname')
            # 本页上所有房子链接的标签

            room_url_list.extend(
                {
                    'city': city,
                    'url': room_url_tag.get('detailurl')
                } for room_url_tag in room_url_tags
            )

        return room_url_list

    def save(self, city, page):
        room_url_list = self.get(city, page)

        with open(url_json_file, 'w', encoding='utf-8') as f:
            print('Dump urls to file')
            json.dump(room_url_list, f)

        from App.mysql import MySQL
        from contextlib import closing

        with closing(MySQL()) as db:
            print('Saving data into database...')
            [db.execute('insert into `urls`(city, url) values ("{city}", "{url}")'.format(
                city=room_url.get('city'),
                url=room_url.get('url')
            )) for room_url in room_url_list]


if __name__ == '__main__':
    url = "http://beijing.xiaozhu.com"
    get_city_room_urls = RoomUrls(url)
    get_city_room_urls.save('北京', 13)
