#!/usr/bin/env python
# coding=utf-8
# this script is used to test package beautifulsoup
import requests
from bs4 import BeautifulSoup

url = 'http://bj.xiaozhu.com/fangzi/6937392816.html'

web_data = requests.get(url)
web_data.encoding = 'utf-8'
soup = BeautifulSoup(web_data.text, 'lxml')

title = soup.select('h4 em')[0].text
gender = 'female' if soup.find_all('div', 'member_ico1') else 'male'

print('title: ', title)
print('gender: ', gender)
print('try to find male: ', soup.find('member_ico'))
