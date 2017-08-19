#!/usr/bin/env python
# coding:utf-8
import threading
import time


def run(n):
    print('Task', n, threading.current_thread())
    time.sleep(2)

start_time = time.time()
threads = []

for i in range(16):
    thread = threading.Thread(target=run, args=('t-{}'.format(i), ))
    thread.start()
    threads.append(thread)

print('Current active threads: ', threading.active_count())
for thread in threads:
    thread.join()

end_time = time.time()
print('All threads has finished...', threading.current_thread())
print('Total cost: ', end_time - start_time)
