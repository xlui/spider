from django.db import models
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

    meta = {'collection': 'Info'}
    # 手动定义 collection name

    def __str__(self):
        return "<Information {}>".format(self.title)


if __name__ == '__main__':
    # default_info = Information(
    #     title="Hello World",
    #     address="Address for default",
    #     price="100",
    #     img="https://www.baidu.com",
    #     hostPic="None",
    #     hostName="default",
    #     hostGender="女"
    # )
    # default_info.save()
    for var in Information.objects.all():
        print(var)
