#!/usr/bin/env python
# coding:utf-8
# 以类的方式使用多线程
import threading
import time


class MyThread(threading.Thread):
    def __init__(self, thread_id, name, delay):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.delay = delay

    def run(self):
        # 必须重载 Thread 类的该方法
        print("start thread:", self.name)
        print_time(self.name, self.delay, 5)
        print("exit thread: " + self.name)


def print_time(thread_name, delay, counter):
    # 输入当前时间 counter 次，并且每次间隔 delay 秒
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
