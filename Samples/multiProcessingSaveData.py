#!/usr/bin/env python
# coding:utf-8
# 通过 多进程/多线程 向数据库写入数据
# 多进程可以成功写入，多线程写入失败。
import threading
from multiprocessing import Pool
import os
import pymongo

data = {}

# for i in range(5):
#     data['_id'] = i
#     data['thread_count'] = i
#     collection.insert(data)


def data_process(count):
    client = pymongo.MongoClient('localhost', 27017)
    xiaozhu = client['xiaozhu']
    # xiaozhu.drop_collection('test')
    collection = xiaozhu['test']

    # data['_id'] = count
    data['thread_count'] = count
    collection.insert(data)
    client.close()

# threads = []
# for i in range(5):
#     thread = threading.Thread(target=data_process, args=(data, i))
#     thread.start()
#     threads.append(thread)
# for thread in threads:
#     thread.join()


pool_count_total = 24
pool = Pool(pool_count_total)
for pool_count in range(pool_count_total):
    pool.apply_async(data_process, args=(pool_count,))
pool.close()
pool.join()
print('All data of process', os.getpid(), 'has been insert into mongodb')
