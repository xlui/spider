#!/usr/bin/env python
# coding: utf-8
# 结合多线程与多进程
from multiprocessing import Pool
import threading
import os


def print_current_thread(process_name):
    # 线程函数
    print('In process {}, current thread is: '.format(process_name), threading.current_thread())


def thread_task(process_name):
    threads = []
    for i in range(13):
        thread = threading.Thread(target=print_current_thread, args=(process_name,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print('In process {}, thread work done.'.format(process_name))


if __name__ == '__main__':
    print('Parent process {}.'.format(os.getpid()))
    pool_count = 24
    pool = Pool(pool_count)
    for i in range(pool_count):
        pool.apply_async(thread_task, args=(i,))
    print('Waiting for all subprocesses done...')
    pool.close()
    pool.join()
    print('All subprocesses done.')
