# test using multiprocess to save data into mongodb
from contextlib import closing
from multiprocessing import Pool
from App.mongodb import MongoDB
from Samples.measure_time import time_func


def run(collection, data):
    with closing(MongoDB()) as mongodb:
        mongodb.save(collection, **data)


@time_func
def main(collection):
    pool_count = 16
    data_count = 10000
    # result:
    # process   data_count  time
    #   1           100         0.7
    #   1           1000        3.21
    #   1           10000       46
    #   4           100         0.41
    #   4           1000        1.6
    #   4           10000       30-40
    #   8           100         0.42
    #   8           1000        1.53
    #   8           10000       35
    #   16          10000       30
    pool = Pool(pool_count)
    list_to_be_saved = [{'page': i, 'url': 'https://www.baidu.com/?page={}'.format(i)} for i in range(data_count)]

    [pool.apply_async(run, args=(collection, list_to_be_saved[i])) for i in range(data_count)]

    print('Waiting for all subprocess to done...')
    pool.close()
    pool.join()
    print('All subprocess done.')
    print('Exit main process.')


if __name__ == '__main__':
    collection = 'test'

    with closing(MongoDB()) as mongodb:
        mongodb.drop(collection)

    main(collection)
