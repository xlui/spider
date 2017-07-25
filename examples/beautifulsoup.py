#!/usr/bin/env python
# coding=utf-8
# this script is used to test package beautifulsoup
import requests
from bs4 import BeautifulSoup


def getGender(soup):
    gender = 'female' if soup.find_all('div', 'member_ico1') else 'male'
    return gender


url = 'http://bj.xiaozhu.com/fangzi/6937392816.html'
web_data = requests.get(url)
web_data.encoding = 'utf-8'
soup = BeautifulSoup(web_data.text, 'lxml')

title = soup.select('h4 em')[0].text
gender = getGender(soup)

print(soup.find('member_ico'))
print(gender)
print(title)
