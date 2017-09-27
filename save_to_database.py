#!/usr/bin/env python
# coding:utf-8
import threading

import pymongo
from Config.config import database, room_url_collection, room_data_collection


class Save(object):
    """
    Class Save: save data to mongo database
    """
    def __init__(self):
        super(Save, self).__init__()
        self.__client = pymongo.MongoClient('localhost', 27017)
        self.__database = self.__client[database]
        self.__data_collection = self.__database[room_data_collection]

    def drop_url(self):
        self.__database.drop_collection(room_url_collection)

    def save_url(self, city_name, url):
        # self.__database.drop_collection(room_url_collection)
        url_collection = self.__database[room_url_collection]
        data = {
            'city_name': city_name,
            'url': url,
        }
        url_collection.insert(data)

    def drop_data(self):
        self.__database.drop_collection(room_data_collection)

    def save_data(self):
        pass

    def disconnect(self):
        self.__client.close()


if __name__ == '__main__':
    # A example to use multithreading to save data into mongodb
    save = Save()

    data_count = 59
    thread_count = 10
    separate = data_count // thread_count

    l = list(range(data_count))
    save.drop_url()

    def save_db(from_, to_):
        sub_list = l[from_:to_]
        for i in sub_list:
            save.save_url('beijing', i)

    threads = []
    for index in range(thread_count):
        if index == (thread_count - 1):
            thread = threading.Thread(target=save_db, args=(index * separate, data_count))
        else:
            thread = threading.Thread(target=save_db, args=(index * separate, index * separate + separate))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    print('Done!')
