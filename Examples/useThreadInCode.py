#!/usr/bin/env python
import threading
import time
import sys
sys.path.append('../')
# add upper folder to use local modules
from getInfo import get_room_url_list
from getRoomInfo import get_room_info


class MyThread(threading.Thread):
    """
    Class MyThread: a class way to use multithreading
    """
    def __init__(self, thread_id_):
        super(MyThread, self).__init__()
        self.thread_id = thread_id_

    def run(self):
        print("start thread: {}".format(self.thread_id))
        print_info(self.thread_id)
        print("exit thread: {}".format(self.thread_id))


def print_info(thread_id_):
    """
    use thread id to separate the room url list

    :param thread_id_: id of the thread
    :return: none
    """
    count = 1
    begin = thread_id_ * separate
    end = thread_id_ * separate + separate
    sub_list = room_url_list[begin: end]

    for room_url in sub_list:
        time.sleep(1)
        room_data = get_room_info(room_url, count + begin)
        print(room_data)
        count += 1


url = "http://bj.xiaozhu.com/search-duanzufang-p1-0/"

room_url_list = get_room_url_list(url, 1)
url_count = len(room_url_list)

thread_count = 3
separate = url_count // thread_count
# fix bug here!
# 24 / 3 = 8.0
# 24 // 3 = 8
start_time = time.time()

# test data valid or not
if url_count == 0:
    print("Cannot access to url!")
    exit(1)
elif url_count % thread_count != 0:
    print("Invalid thread number!")
    exit(2)
else:
    print("success")

threads = []
# start threads
for thread_id in range(thread_count):
    thread_tmp = MyThread(thread_id)
    thread_tmp.start()
    threads.append(thread_tmp)
for thread in threads:
    thread.join()

print("exit main thread")
stop_time = time.time()
print("total run time: {}s.".format(round(stop_time - start_time)))
