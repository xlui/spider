from django.db import models
from mongoengine import connect, Document, StringField
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

    meta = {'collection': 'room_data'}


if __name__ == '__main__':
    print(Information.objects.count())
