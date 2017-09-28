#!/usr/bin/env python
# coding:utf-8
# use crossincode's api to get proxy ip
import json
import requests

url = 'http://lab.crossincode.com/proxy/get/?num=5&head=http'

data = requests.get(url)
data.encoding = 'utf-8'
data_dict = eval(data.text)

proxies = [proxies.get('http') for proxies in data_dict.get('proxies')]

with open('proxies.json', 'w', encoding='utf-8') as file:
    json.dump(proxies, file)

print(proxies)
