#!/usr/bin/env python
# coding:utf-8
# 使用线程锁的实例
import threading
from time import time
from random import seed, randint

lock = threading.Lock()
balance = 0
total_range = 100000


def change(n):
    global balance
    balance = balance + n
    balance = balance - n


def run_thread1(number):
    # 不使用线程锁
    [change(number) for _ in range(total_range)]


def run_thread2(number):
    # 使用线程锁
    for i in range(100000):
        lock.acquire()
        try:
            change(number)
        finally:
            lock.release()


target = run_thread1
# 将 target 的值设置为不同的函数来显示两种情况下的结果
thread_count = 16
threads = []
seed(time())
for i in range(thread_count):
    thread = threading.Thread(target=target, args=(randint(1, 10), ))
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()

print('Balance should be 0.')
print('Balance:', balance)
