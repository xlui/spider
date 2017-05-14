#!/usr/bin/env python
# coding=utf-8
from mongoengine import *
connect('xiaozhu')

class Information(Document):
    _id = StringField()
    title = StringField()
    address = StringField()
    price = StringField()
    img = StringField()
    hostPic = StringField()
    hostName = StringField()
    hostGender = StringField()

    meta = {'collection': 'Info_new'}

# get all data
l = []
for var in Information.objects:
    l.append(var.title)
print(l)
print(len(l))
