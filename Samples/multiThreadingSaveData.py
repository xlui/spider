# test using multithreading to save data into mongodb
# And the result show for-loop run faster
import threading
import pymongo
from time import time
from functools import wraps


client = pymongo.MongoClient('localhost', 27017)
database = client['test']
collection = database['test']
data_count = 100000
list_to_be_saved = [i for i in range(data_count)]


def time_func(func):
    @wraps(func)
    def measure_time(*args, **kwargs):
        time_start = time()
        print('@time_func: start function [{}]'.format(func.__name__))
        result = func(*args, **kwargs)
        time_stop = time()
        print('@time_func: stop function [{}]'.format(func.__name__))
        print('@time_func: function [{}] takes'.format(func.__name__),
              (time_stop - time_start), 'seconds.')
        return result
    return measure_time


@time_func
def use_multithreading():
    list_count = len(list_to_be_saved)
    thread_count = 8
    separate = data_count // thread_count
    threads = []

    def save_to_db(from_, to_):
        sub_list = list_to_be_saved[from_: to_]
        [collection.insert_one({'number': i}) for i in sub_list]

    for thread_index in range(thread_count):
        if thread_index == (thread_count - 1):
            thread = threading.Thread(target=save_to_db, args=(
                thread_index * separate, list_count))
        else:
            thread = threading.Thread(target=save_to_db,
                                      args=(thread_index * separate,
                                            thread_index * separate +
                                            separate))
        thread.start()
        threads.append(thread)
    [thread.join() for thread in threads]


@time_func
def not_use():
    [collection.insert_one({'number': i}) for i in list_to_be_saved]


def main():
    database.drop_collection('test')
    use_multithreading()
    # 30 seconds
    database.drop_collection('test')
    not_use()
    # 25 seconds


if __name__ == '__main__':
    main()
