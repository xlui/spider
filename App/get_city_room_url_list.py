#!/usr/bin/env python
# coding:utf-8
# use multithreading to get a city's room url list from a city url
import requests
import threading
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from Config.config import headers, headers_length, proxies, proxies_length


class GetCityRoomUrlList(object):
    """Class GetCityRoomList -- get all room list of a city"""
    def __init__(self, city_url):
        super(GetCityRoomUrlList, self).__init__()
        self.__page_base_url = city_url + "/search-duanzufang-p{}-0/"
        self.__room_url_dict = {}

    def get(self, page=14):
        threads = []
        for page_index in range(1, page):
            # for each page, start a new thread to get room url list
            thread = threading.Thread(target=run, args=(page_index, self.__page_base_url, self.__room_url_dict))
            thread.start()
            threads.append(thread)
        print('Now active threads: ', threading.active_count())
        [thread.join() for thread in threads]

        room_url_list = [room_url for value in self.__room_url_dict.values() for room_url in value]
        # get room url list from dict, use list comp to speed up
        self.__room_url_dict= {}
        return room_url_list


def run(thread_id, page_base_url, room_url_dict):
    page_url = page_base_url.format(thread_id)
    # get page url for stationary format
    sleep(randint(2, 20))
    # sleep between each thread
    web_data = requests.get(page_url,
                            headers=headers[randint(0, headers_length - 1)],
                            proxies=proxies[randint(0, proxies_length - 1)])
    sleep(randint(0, 20))
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'lxml')
    room_url_list_tag = soup.select('div.result_btm_con.lodgeunitname')
    # this selects all the room url tags in a page

    for room_url_tag in room_url_list_tag:
        room_url_dict.setdefault(thread_id, []).append(room_url_tag.get('detailurl'))
        # save data into a dict, use `thread_id` as the `key`
    print('Page {}: get room url list {}'.format(thread_id, 'done' if room_url_dict else 'false'))


if __name__ == '__main__':
    city_url = "http://beijing.xiaozhu.com"
    get_city_room_url_list = GetCityRoomUrlList(city_url)
    room_url_list_ = get_city_room_url_list.get()
    print('\nroom url list: ')
    [print(room_url) for room_url in room_url_list_]
    print('Total: {} room urls.'.format(len(room_url_list_)))
