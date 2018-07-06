# todo: Use thread class instead of thread code to avoid to many repeated codes.
# class method to use multithreading
import threading
# from Samples.measure_time import time_func


class MyThread(threading.Thread):
    def __init__(self, thread_id, func, **func_args):
        super(MyThread, self).__init__()
        self.__thread_id = thread_id
        self.__func = func
        self.__func_args = func_args

    def run(self):
        print('Start thread', self.__thread_id)
        self.__func(**self.__func_args)
        print('Stop thread', self.__thread_id)

    @staticmethod
    def separate(count, func, _list):
        """separate method is used to deal with `same works on a long list`,
        separate the long list to stable pieces, and use multi-threading to work for each pieces.

        :param count: count of threads you want
        :param func: function that do works on the list
        :param _list: the origin list
        :return: None.
        """
        total_count = len(_list)
        separate = total_count // count
        threads = []

        def thread_function(_from, _to):
            sub_list = _list[_from: _to]
            for item in sub_list:
                func(item, )

        for index in range(count):
            if index == (count - 1):
                thread = MyThread(index, thread_function, from_=index * separate, to_=total_count)
            else:
                thread = MyThread(index, thread_function, from_=index * separate, to_=(index * separate + separate))
            thread.start()
            threads.append(thread)
        [thread.join() for thread in threads]
        print("All threads's work Done!")


# @time_func
def main():
    from app.mongodb import MongoDB
    from contextlib import closing

    collection = 'test'
    data_count = 40000
    url_to_be_saved = [{'page': i, 'url': 'https://www.baidu.com/?page={}'.format(i)} for i in range(data_count)]

    with closing(MongoDB()) as mongodb:
        mongodb.drop(collection)

    def save_function(item):
        with closing(MongoDB()) as mongodb:
            mongodb.save(collection, **item)

    MyThread.separate(8, save_function, url_to_be_saved)
    # single thread: 28 seconds
    # 20+ threads: 35 seconds


if __name__ == '__main__':
    main()
