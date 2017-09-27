#!/usr/bin/env python
# coding:utf-8
# 以代码的形式使用多线程
import threading
import time


def run(n):
    # 线程函数
    print('Task', n, threading.current_thread())
    time.sleep(2)


start_time = time.time()
threads = []
thread_count = 16
for i in range(thread_count):
    thread = threading.Thread(target=run, args=('t-{}'.format(i), ))
    thread.start()
    threads.append(thread)

print('Current active threads: ', threading.active_count())
for thread in threads:
    thread.join()

end_time = time.time()
print('All threads has finished...')
print('Each thread should sleep 2 seconds, and the Main Thread will wait for all threads done.')
print('Total cost time: ', end_time - start_time)
