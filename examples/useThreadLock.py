#!/usr/bin/env python
# use thread
import threading
import time
import pymongo
from getInfo import get_room_url_list
from getRoomInfo import get_room_info


class MyThread(threading.Thread):
    """docstring for MyThread"""

    def __init__(self, threadID):
        super(MyThread, self).__init__()
        self.threadID = threadID

    def run(self):
        print("start thread: {}".format(self.threadID))
        room_data_list = print_info(self.threadID)
        threadLock.acquire()
        for room_data in room_data_list:
            table.insert_one(room_data)
        threadLock.release()
        print("exit thread: {}".format(self.threadID))


def print_info(threadID):
    count = 1
    room_data_list = []
    separate = urlCount // threadCount
    # fix bug here!
    # 24 / 3 = 8.0
    # 24 // 3 = 8
    begin = threadID * separate
    end = threadID * separate + separate
    sub_list = room_url_list[begin: end]

    for room_url in sub_list:
        time.sleep(1)
        room_data_list.append(get_room_info(room_url, count + begin))
        # print(room_data)
        count += 1

    return room_data_list


threadCount = 24
threadLock = threading.Lock()
threads = []
url = "http://bj.xiaozhu.com/search-duanzufang-p1-0/"
client = pymongo.MongoClient('localhost', 27017)
db = client['db_test']
table = db['tb_test']

room_url_list = get_room_url_list(url, 1)
urlCount = len(room_url_list)
start_time = time.time()

# test data
if urlCount == 0:
    print("Cannot access to url!")
    exit(1)
elif urlCount % threadCount != 0:
    print("Invalid thread number!")
    exit(2)
else:
    print("succ")

# start thread
for index in range(threadCount):
    thread_tmp = MyThread(index)
    thread_tmp.start()
    threads.append(thread_tmp)

for thread in threads:
    thread.join()

print("exit main thread")

stop_time = time.time()
print("total run time: {}".format(round(stop_time - start_time)))
