#!/usr/bin/env python
import threading
import time


class myThread(threading.Thread):
    """docstring for myThread"""

    def __init__(self, threadID, name, counter):
        super(myThread, self).__init__()
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("start thread: " + self.name)
        threadLock.acquire()
        # get lock
        print_time(self.name, self.counter, 3)
        threadLock.release()
        # release lock


def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print("%s %s" % (threadName, time.ctime(time.time())))
        counter -= 1


threadLock = threading.Lock()
threads = []

for index in range(2):
    thread_tmp = myThread(index, "Thread-%d" % index, 1)
    thread_tmp.start()
    threads.append(thread_tmp)

for thread in threads:
    thread.join()

print("exit main thread")
