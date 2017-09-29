from time import time
from functools import wraps


def time_func(func):
    @wraps(func)
    def measure_time(*args, **kwargs):
        time_start = time()
        result = func(*args, **kwargs)
        time_stop = time()
        print('@time_func: function [{}] takes'.format(func.__name__), (time_stop - time_start), 'seconds.')
        return result
    return measure_time
