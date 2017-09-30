from django.db import models
from mongoengine import connect, Document, StringField
connect('xiaozhu')


class Data(Document):
    _id = StringField()
    title = StringField()
    address = StringField()
    price = StringField()
    img = StringField()
    host_pic = StringField()
    host_name = StringField()
    host_gender = StringField()

    meta = {'collection': 'room_data'}


if __name__ == '__main__':
    print(Data.objects.count())
