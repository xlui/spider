#!/usr/bin/env python
# coding:utf-8
import threading
import pymongo
from Config.config import db_url, db_port, database


class MongoDB(object):
    """Class Save: save data to mongo database"""
    def __init__(self):
        super(MongoDB, self).__init__()
        self.__client = pymongo.MongoClient(db_url, db_port)
        self.__database = self.__client[database]

    def drop(self, collection):
        # drop collection from database
        result = self.__database.drop_collection(collection)
        if result.get('ok'):
            print('Successfully drop collection `{}` from MongoDB'.format(collection))
            return 1
        else:
            print('Failed to drop collection `{}` from MongoDB, collection may not exist.'.format(collection))
            return 0

    def save(self, collection, **kwargs):
        db_collection = self.__database[collection]
        data = {**kwargs}
        return db_collection.insert_one(data)

    def print(self, collection):
        print('Data in collection `{}` is:'.format(collection))
        db_collection = self.__database[collection]
        documents = db_collection.find()
        for document in documents:
            print(document)
        print('Total:', documents.count(), 'documents.')

    def close(self):
        self.__client.close()


if __name__ == '__main__':
    # A example to use multithreading to save data into mongodb
    save = MongoDB()

    data_count = 59
    thread_count = 10
    threads = []
    separate = data_count // thread_count
    collection = 'test'

    total_list = list(range(data_count))
    save.drop(collection)

    def save_db(from_, to_):
        sub_list = total_list[from_:to_]
        for i in sub_list:
            save.save(collection, url_count=i, url='https://www.baidu.com/?page={}'.format(i))

    # start multithreading
    for index in range(thread_count):
        if index == (thread_count - 1):
            thread = threading.Thread(target=save_db, args=(index * separate, data_count))
        else:
            thread = threading.Thread(target=save_db, args=(index * separate, index * separate + separate))
        thread.start()
        threads.append(thread)
    [thread.join() for thread in threads]

    print("All threads' work Done!")

    save.print(collection)
    save.close()
