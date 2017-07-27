#!/usr/bin/env python
#coding:utf-8
# thread module
import threading 
import time

class SaveThread(threading.Thread):
    """Save Thread, used to speed up save progress"""
    def __init__(self, sub_room_url_list, thread_id):
        super(SaveThread, self).__init__()
        self.sub_room_url_list = sub_room_url_list
        self.thread_id = thread_id

    def run(self):
        print('start thread:', self.thread_id, time.ctime())
        save_data(self.sub_room_url_list)
        print('stop thread:', self.thread_id, time.ctime())


def save_data(room_url_list):
    pass