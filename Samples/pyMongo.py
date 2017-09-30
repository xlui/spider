#!/usr/bin/env python
# coding:utf-8
from time import time
import pymongo
from Config.config import database, test_collection

client = pymongo.MongoClient('localhost', 27017)
# database client
xiaozhu = client[database]
# connect to database or create database

# xiaozhu.drop_collection(sample_collection)
# remove collection

collection = xiaozhu[test_collection]
# create collection

data = {
    'name': 'test1',
    'value': 'www.beijing.com',
    'time': time()
}

# insert
collection.insert_one(data)

# output
print(list(collection.find()))

# print(collection.insert_one(data).inserted_id)
# print(collection.find_one())
