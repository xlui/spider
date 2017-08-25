#!/usr/bin/env python
# coding: utf-8
from multiprocessing import Pool
import threading
import os
import time
import random


def print_current_thread(process_name):
    print('In process {}, current thread is: '.format(process_name), threading.current_thread())


def thread_task(process_name):
    threads = []
    for i in range(5):
        thread = threading.Thread(target=print_current_thread, args=(process_name,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print('In process {}, thread work done.'.format(process_name))


if __name__ == '__main__':
    print('Parent process {}.'.format(os.getpid()))
    pool = Pool(3)
    for i in range(3):
        pool.apply_async(thread_task, args=(i,))
    print('Waiting for all subprocesses done...')
    pool.close()
    pool.join()
    print('All subprocesses done.')
