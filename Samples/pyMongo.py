#!/usr/bin/env python
# coding:utf-8
import pymongo
from conf.config import database, room_data_collection

client = pymongo.MongoClient('localhost', 27017)
# database client
xiaozhu = client[database]
# use database or create database
xiaozhu.drop_collection(room_data_collection)
# remove collection
info = xiaozhu[room_data_collection]
# create collection

data = {
    'name':'test1',
    'value':'www.beijing.com',
}

info.insert_one(data)
