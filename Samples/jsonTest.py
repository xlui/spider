#!/usr/bin/env python
# coding:utf-8
# 以 Json 的格式保存数据；从 Json 文件中读取数据
import json

data = [
    {'name':'beijing', 'city':'www.beijing.com'},
    {'name':'shanghai', 'city':'www.shanghai.com'},
]

with open('test_json.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file)

with open('test_json.json', 'r', encoding='utf-8') as json_file:
    read_data = json.load(json_file)

print('print read data: ', read_data)
print('read data type: ', type(read_data))
# list
for data in read_data:
    print('list element type: ', type(data))
    # dict
    print('list element', data)
