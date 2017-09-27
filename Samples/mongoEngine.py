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
    # 默认情况下，类名就是 collection 名。
    # 不过你也可以通过以下代码手动指定 collection name
    # meta = {'collection': 'New_Table_Name'}
    name = StringField(max_length=10, required=True)
    data = IntField(default=0, required=True)
    date = DateTimeField(default=datetime.now(), required=True)


# 插入数据
info = Information(name="Linux", data=datetime.utcnow())
info.save()

# 输入所有数据
list_of_data = [var.name for var in Information.objects]
print(list_of_data)
print('len of list is %d' % len(list_of_data))

# 查询
query = Information.objects(name="Linux")
for var in query:
    print("the date of {} is {}".format(var.name, var.date))
