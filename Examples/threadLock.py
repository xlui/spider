#!/usr/bin/env python
# coding:utf-8
# Example to show how to use thread lock
import threading

lock = threading.Lock()
balance = 0


def change(n):
    global balance
    balance = balance + n
    balance = balance - n


def run_thread1(number):
    """
    Do not use thread lock, the result of balance is unpredictable
    :param n: number to add and sub
    :return: none
    """
    for i in range(100000):
        change(number)

def run_thread2(number):
    """
    Use thread lock, the result of balance is 0
    :param number: number to add and sub
    :return: none
    """
    for i in range(100000):
        lock.acquire()
        try:
            change(number)
        finally:
            lock.release()


target = run_thread1
thread1 = threading.Thread(target=target, args=(5, ))
thread2 = threading.Thread(target=target, args=(8, ))
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print(balance)