# todo: Use thread class instead of thread code to avoid to many repeated codes.
# class method to use multithreading
import threading
from Samples.measure_time import time_func


class MyThread(threading.Thread):
    def __init__(self, thread_id, thread_func, **thread_func_args):
        super(MyThread, self).__init__()
        self.__thread_id = thread_id
        self.__thread_func = thread_func
        self.__thread_func_args = thread_func_args

    def run(self):
        print('Start thread', self.__thread_id)
        self.__thread_func(**self.__thread_func_args)
        print('Stop thread', self.__thread_id)

    @staticmethod
    def SeparateListMultiThread(thread_count, function_, arg_list):
        """SeparateListMultiThread static method is used to deal with same works on a long list,
        separate the long list to stable pieces, and use multithreading to work for the pieces.
        Params you should provided is the thread count you want, function that do works on the list,
        and finally, the origin list

        :param thread_count: count of threads you want
        :param function_: function that do works on the list
        :param arg_list: the origin list
        :return: None.
        """
        total_count = len(arg_list)
        separate = total_count // thread_count
        threads = []

        def thread_function(from_, to_):
            sub_list = arg_list[from_: to_]
            for item in sub_list:
                function_(item, )

        for index in range(thread_count):
            if index == (thread_count - 1):
                thread = MyThread(index, thread_function, from_=index * separate, to_=total_count)
            else:
                thread = MyThread(index, thread_function, from_=index * separate, to_=(index * separate + separate))
            thread.start()
            threads.append(thread)
        [thread.join() for thread in threads]
        print("All threads's work Done!")


@time_func
def main():
    from App.mongodb import MongoDB
    from contextlib import closing

    collection = 'test'
    data_count = 40000
    url_to_be_saved = [{'page': i, 'url': 'https://www.baidu.com/?page={}'.format(i)} for i in range(data_count)]

    with closing(MongoDB()) as mongodb:
        mongodb.drop(collection)

    def save_function(item):
        with closing(MongoDB()) as mongodb:
            mongodb.save(collection, **item)

    MyThread.SeparateListMultiThread(8, save_function, url_to_be_saved)
    # single thread: 28 seconds
    # 20+ threads: 35 seconds


if __name__ == '__main__':
    main()
