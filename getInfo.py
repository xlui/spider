#!/usr/bin/env python
# coding=utf-8
import requests
import time
import pymongo
from bs4 import BeautifulSoup
from getCityInfo import get_city_url
# import to use get_city_info method to city url from main site
from getRoomInfo import get_room_info
# import to use get_room_info method to get detail room info


def get_room_url_list(page_url, page_index):
    # get exact room urls from a page
    room_url_list = []
    web_data = requests.get(page_url)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'lxml')
    room_info_list = soup.select('div.result_btm_con.lodgeunitname')
    for room_info in room_info_list:
        room_url_list.append(room_info.get('detailurl'))
    print('Page %d: get room list urls Done!' % (page_index))
    return room_url_list


def get_page_info(startPage, endPage, baseURL, database):
    # get all rental information of a city a save into MongoDB
    # through watching the urls of a city's rental info,
    # there are 13 pages of information for a city
    # just like city beijing, page: bj.xiaozhu.com
    # the first page is: http://bj.xiaozhu.com/search-duanzufang-p1-0/
    # and the last page is: http://bj.xiaozhu.com/search-duanzufang-p13-0/
    count = 1
    room_url_list = []
    for page_index in range(startPage, endPage + 1):
        time.sleep(0.1)
        page_url = baseURL.format(page_index)
        room_url_list += get_room_url_list(page_url, page_index)
        # for each page of city, get the exact url of room
    for room_url in room_url_list:
        time.sleep(0.1)
        # sleep to avoid too frequent access
        data = get_room_info(room_url, count)
        database.insert_one(data)
        count += 1
    print('one page data have been inserted into database!')


def main():
    baseUrl = 'http://www.xiaozhu.com/'
    client = pymongo.MongoClient('localhost', 27017)
    xiaozhu = client['xiaozhu']
    xiaozhu.drop_collection('Info')
    print("drop collection from database xiaozhu!")
    count = 0
    try:
        Info = xiaozhu['Info']

        cities, cityName = get_city_url(baseUrl)
        for city in cities:
            print('Get Info of city: %s, number: %d of total 24' %
                  (cityName[count], count + 1))
            pageBaseUrl = city + 'search-duanzufang-p{}-0/'
            get_page_info(1, 13, pageBaseUrl, Info)
            count += 1
            time.sleep(3)
            # sleep to avoid too frequent access
        print("All data has been insert into mongodb")
    except KeyboardInterrupt:
        print("Keyboard Interrupt!")


if __name__ == "__main__":
    main()
