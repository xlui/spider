#!/usr/bin/env python
# coding=utf-8
import requests
import time
import pymongo
import threading
from bs4 import BeautifulSoup
from getCityInfo import get_city_url
# import to use get_city_info method to city url from main site
from getRoomInfo import get_room_info
# import to use get_room_info method to get detail room info


# global variables
thread_count = 100
client = pymongo.MongoClient('localhost', 27017)
xiaozhu = client['xiaozhu']
xiaozhu.drop_collection('Info')
info = xiaozhu['Info']


class MyThread(threading.Thread):
    """docstring for MyThread"""

    def __init__(self, sub_room_url_list, thread_id, begin):
        super(MyThread, self).__init__()
        self.sub_room_url_list = sub_room_url_list
        self.thread_id = thread_id
        self.begin = begin

    def run(self):
        print('start thread:', self.thread_id, time.ctime())
        save_data(self.sub_room_url_list, self.begin)
        print('stop thread:', self.thread_id, time.ctime())


def save_data(sub_room_url_list, begin):
    count = 1
    for room_url in sub_room_url_list:
        time.sleep(3)
        room_data = get_room_info(room_url, count + begin)
        info.insert_one(room_data)
        count += 1


def call_thread(room_url_list):
    threads = []
    url_count = len(room_url_list)
    separate = url_count // thread_count

    # if url_count == 0:
    #     print('Cannot access to url!')
    #     exit(1)
    # elif url_count % thread_count != 0:
    #     print('Invalid thread number!')
    #     exit(2)

    for index in range(thread_count):
        begin = index * separate
        end = index * separate + separate
        sub_list = room_url_list[begin:end]
        thread_tmp = MyThread(sub_list, index, begin)
        thread_tmp.start()
        threads.append(thread_tmp)

    for thread in threads:
        thread.join()


def get_room_url_list(page_url, page_index):
    # get exact room urls from a page
    room_url_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    }
    web_data = requests.get(page_url, headers=headers)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'lxml')
    room_info_list = soup.select('div.result_btm_con.lodgeunitname')
    for room_info in room_info_list:
        room_url_list.append(room_info.get('detailurl'))
    print('Page %d: get room list urls Done!' % (page_index))
    return room_url_list


def get_page_info(startPage, endPage, baseURL):
    # get all rental information of a city a save into MongoDB
    # through watching the urls of a city's rental info,
    # there are 13 pages of information for a city
    # just like city beijing, page: bj.xiaozhu.com
    # the first page is: http://bj.xiaozhu.com/search-duanzufang-p1-0/
    # and the last page is: http://bj.xiaozhu.com/search-duanzufang-p13-0/
    room_url_list = []
    for page_index in range(startPage, endPage + 1):
        time.sleep(3)
        page_url = baseURL.format(page_index)
        room_url_list += get_room_url_list(page_url, page_index)
        # for each page of city, get the exact url of room

    call_thread(room_url_list)

    print('one page data have been inserted into database!')


def main():
    baseUrl = 'http://www.xiaozhu.com/'
    count = 0
    try:
        cities, city_name = get_city_url(baseUrl)
        for city in cities:
            print('Get Info of city: %s, number: %d of total 24' %
                  (city_name[count], count + 1))
            pageBaseUrl = city + 'search-duanzufang-p{}-0/'
            get_page_info(1, 13, pageBaseUrl)
            count += 1
            time.sleep(3)
            # sleep to avoid too frequent access
        print("All data has been insert into mongodb")
    except KeyboardInterrupt:
        print("Keyboard Interrupt!")


if __name__ == "__main__":
    main()
