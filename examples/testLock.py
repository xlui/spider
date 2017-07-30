#!/usr/bin/env python
# coding=utf-8
# desc: this program is used to test when using multithread to write data into
# mongodb, the main program need thread lock or not, and the result shows it
# does not need.
import threading
import pymongo
import time


class MyThread(threading.Thread):
    """test insert into mongodb"""

    def __init__(self, count):
        super(MyThread, self).__init__()
        self.count = count

    def run(self):
        print("start thread: ", self.count, time.ctime(time.time()))
        thread_function(self.count)
        print("stop thread: ", self.count, time.ctime(time.time()))


def thread_function(count):
    ret = {
        'serial': count,
    }
    table.insert_one(ret)


threads = []
start_time = time.time()
client = pymongo.MongoClient('localhost', 27017)
db = client['test']
db.drop_collection('testLock')
# drop exist table
table = db['testLock']

thread_number = int(input('> please input the number of threads: '))
for index in range(thread_number):
    thread_tmp = MyThread(index)
    thread_tmp.start()
    threads.append(thread_tmp)
for thread in threads:
    thread.join()
print('exit main thread')
end_time = time.time()
print('total time: ', round(end_time - start_time))
