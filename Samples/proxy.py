#!/usr/bin/env python
# coding:utf-8
import requests
import os
import sys
sys.path.append('../')
from conf.config import headers, proxies


url = 'http://bj.xiaozhu.com/fangzi/6937392816.html'
response = requests.get(url, headers=headers, timeout=10, proxies=proxies)
print(response.text)
