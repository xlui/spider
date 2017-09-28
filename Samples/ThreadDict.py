#!/usr/bin/env python
# coding:utf-8
# insert data into dict through multithreading
from random import randint
import threading


def run(thread_id):
    dic[thread_id] = ['https://www.baidu.com/?page={}'.format(i) for i in range(randint(0, 4))]


dic = {}
thread_count = 5
threads = []
for i in range(thread_count):
    thread = threading.Thread(target=run, args=(i, ))
    thread.start()
    threads.append(thread)
[thread.join() for thread in threads]

print("All threads' work Done!")

print('dic:')
for key, value in dic.items():
    print(key, value)
print()

final_list = [list_ for value in dic.values() for list_ in value]
print('final list:', final_list)
print('length of final list:', len(final_list))
