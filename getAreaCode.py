#!/usr/bin/env python
# coding=utf-8
from models import *

cityCodeDict = {
    '北京': 'bj',
    '上海': 'sh',
    '南京': 'nj',
    '成都': 'cd',
    '广州': 'gz',
    '重庆': 'cq',
    '武汉': 'wh',
    '大连': 'dl',
    '三亚': 'sanya',
    '丽江': 'lijiang',
    '天津': 'tj',
    '香港': 'xianggang',
    '长沙': 'cs',
    '无锡': 'wx',
    '昆明': 'km',
    '济南': 'jn',
    '厦门': 'xm',
    '青岛': 'qd',
    '郑州': 'zz',
    '西安': 'xa',
    '杭州': 'hz',
    '深圳': 'sz',
    '沈阳': 'sy',
    '苏州': 'sz'
}

# query in mongoengine
for obj in Information.objects(hostName="childskins"):
    print(cityCodeDict[obj.address[0:3]])

