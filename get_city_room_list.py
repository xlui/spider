#!/usr/bin/env python
# coding:utf-8
# use thread to get a city's room url list, provide get() method to return result list
import requests
from bs4 import BeautifulSoup
import threading
from random import randint
from time import sleep
from conf.config import headers, proxies


class GetCityRoomUrlList(object):
    """
    Class GetCityRoomList -- get all room list of a city
    """
    def __init__(self, city):
        super(GetCityRoomUrlList, self).__init__()
        self.__page_base_url = city + "search-duanzufang-p{}-0/"

    def get(self):
        """Use multithreading to get all pages' data

        :return: one city's room url list
        """
        threads = []
        global room_url_list
        for page_index in range(1, 14):
            thread = threading.Thread(target=run, args=(page_index, self.__page_base_url))
            thread.start()
            threads.append(thread)
        print('Active threads: ', threading.active_count())
        for thread in threads:
            thread.join()
        return room_url_list


def run(thread_id, page_base_url):
    page_url = page_base_url.format(thread_id)
    time_to_sleep = randint(0, 4)
    sleep(time_to_sleep)
    web_data = requests.get(page_url, headers=headers, proxies=proxies)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'lxml')
    room_url_list_label = soup.select('div.result_btm_con.lodgeunitname')

    # global room_url_list
    for room_url_label in room_url_list_label:
        lock.acquire()
        try:
            room_url_list.append(room_url_label.get('detailurl'))
        finally:
            lock.release()
    print('Page {}: get room url list done!'.format(thread_id))


room_url_list = []
lock = threading.Lock()

if __name__ == '__main__':
    city_url = "http://sy.xiaozhu.com/"
    # room_url_list = []
    get_city_room_url_list = GetCityRoomUrlList(city_url)
    room_url_list_ = get_city_room_url_list.get()
    print('\nroom url list: ')
    for room_url in room_url_list_:
        print(room_url)
    print('Total: {}'.format(len(room_url_list_)))
