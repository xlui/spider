#!/usr/bin/env python
# coding:utf-8
# 使用代理的实例
import requests
import sys
sys.path.append('../')
from Config.config import headers, proxies


url = 'http://bj.xiaozhu.com/fangzi/6937392816.html'
response = requests.get(url, headers=headers, timeout=10, proxies=proxies)
print(response.text)
