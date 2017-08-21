#!/usr/bin/env python
# coding:utf-8
import requests
import os
import sys
sys.path.append('../')
from conf.config import headers, proxies


url = 'http://www.xiaozhu.com/'
response = requests.get(url, headers=headers, timeout=10, proxies=proxies)
print(response.text)
