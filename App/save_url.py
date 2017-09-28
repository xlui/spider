#!/usr/bin/env python
# coding:utf-8
import threading
from multiprocessing import Pool
from random import randint
from time import sleep

from App.get_city_room_url_list import GetCityRoomUrlList
from App.get_cities import GetCities
from App.mongodb import MongoDB
from Config.config import room_url_collection


def get_list_and_save(city_):
    get_city_room_url_list = GetCityRoomUrlList(city_.get('url'))

    # sleep to avoid being blocked -- Multi Processes Case
    # sleep(randint(0, 20))
    room_url_list = get_city_room_url_list.get()
    # Now, variable `room_url_list` stores all the rental room's url
    # sleep(randint(0, 10))

    # open database connect
    database = MongoDB()

    list_count = len(room_url_list)
    # total urls
    thread_count = 20
    # total threads
    threads = []
    separate = list_count // thread_count
    city_name = city_.get('name')

    # for i in range(list_count):
    #     database.save(room_url_collection, city_name=city_name, url=room_url_list[i])

    def save_to_db(from_, to_):
        sub_list = room_url_list[from_:to_]
        [database.save(room_url_collection, city_name=city_name, room_url=room_url) for room_url in sub_list]

    for thread_index in range(thread_count):
        if thread_index == (thread_count - 1):
            thread = threading.Thread(target=save_to_db, args=(thread_index * separate, list_count))
        else:
            thread = threading.Thread(target=save_to_db, args=(thread_index * separate,
                                                               thread_index * separate + separate))
        thread.start()
        threads.append(thread)
    [thread.join() for thread in threads]

    database.save(collection='Overview', city_name=city_name, total_urls=list_count)
    database.close()

    print('Total: {} urls'.format(list_count))
    global count
    print('All room url of city', city_name, '(count {}/{}) has been saved into database!'.format(count, total_count))
    count += 1


if __name__ == '__main__':
    from contextlib import closing
    with closing(MongoDB()) as db:
        db.drop(room_url_collection)
        db.drop(collection='Overview')

    cities = GetCities().get()
    count = 1
    total_count = len(cities)
    # pool = Pool(24)
    # for city in cities:
    #     pool.apply_async(get_list_and_save, args=(city, ))
    # pool.close()
    # pool.join()
    # print('All subprocesses done.')
    [get_list_and_save(city) for city in cities]
