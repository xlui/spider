#!/usr/bin/env python
# coding: utf-8
# get detail information of rooms from url, also will output the
# number of data
import requests
from bs4 import BeautifulSoup


def get_room_info(room_url, count):
    # get detail info of room and return a list
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    }
    web_data = requests.get(room_url, headers=headers)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'lxml')

    title = soup.select('h4 em')[0].text
    try:
        address = soup.select('span.pr5')[0].text
    except IndexError:
        address = None
    price = soup.select('div.day_l span')[0].text
    img = soup.select('#curBigImage')[0].get('src')
    hostPic = soup.select('div.member_pic a img')[0].get('src')
    hostName = soup.select('h6 a.lorder_name')[0].text
    hostGender = 'female' if soup.find_all('div', 'member_ico1') else 'male'

    data = {
        'title': title,
        'address': address,
        'price': price,
        'img': img,
        'hostPic': hostPic,
        'hostName': hostName,
        'hostGender': hostGender
    }
    print('get base info %d Done!' % (count))
    return data


if __name__ == '__main__':
    room_url = "http://bj.xiaozhu.com/fangzi/14936062703.html"
    count = 0
    data = get_room_info(room_url, count)
    print(data)
