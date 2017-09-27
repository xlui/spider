#!/usr/bin/env python
# coding:utf-8
import threading
import time


class MyThread(threading.Thread):
    """
    Class way to call multithreading
    """
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        """
        must have this func in class

        :return: none
        """
        print("start thread:", self.name)
        print_time(self.name, self.counter, 5)
        print("exit thread: " + self.name)


def print_time(thread_name, delay, counter):
    """
    play current time COUNTER times, and sleep DELAY during each loop

    :param thread_name: the name of this thread
    :param delay: sleep between each loop
    :param counter: count of print
    :return: none
    """
    while counter:
        time.sleep(delay)
        print("%s %s" % (thread_name, time.ctime()))
        counter -= 1

if __name__ == '__main__':
    thread1 = MyThread(1, "Thread-1", 1)
    thread2 = MyThread(2, "Thread-2", 2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("exit main thread")
