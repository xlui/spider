#!/usr/bin/env python
# coding=utf-8
from mongoengine import *
from datetime import datetime

# connect('xiaozhu')
# if u need to authorization and specify a hostname use:
# connect('xiaozhu', host='192.168.1.1', username='root', password='1234')
#
# class Information(Document):
#     _id = StringField()
#     title = StringField()
#     address = StringField()
#     price = StringField()
#     img = StringField()
#     hostPic = StringField()
#     hostName = StringField()
#     hostGender = StringField()
#
#     meta = {'collection': 'Info_new'}
#     # specify a table name
#
# get all data
# if __name__ == '__main__':
#     list_of_data = []
#     for var in Information.objects:
#         list_of_data.append(var.title)
#     print(list_of_data)
#     print(len(list_of_data))


connect("test")


class Information(Document):
    # By default, a class name is also a table name
    # But u can specify a table name use meta:
    # meta = {'collection': 'New_Table_Name'}
    name = StringField(max_length=10, required=True)
    data = IntField(default=0, required=True)
    date = DateTimeField(default=datetime.now(), required=True)


# insert
info = Information(name="Linux", data=2017)
info.save()

# output table
list_of_data = []
for var in Information.objects:
    list_of_data.append(var.name)
print(list_of_data)
print('len of list is %d' % len(list_of_data))

# query
query = Information.objects(name="Linux")
for var in query:
    print("the date of {} is {}".format(var.name, var.date))
