#!/usr/bin/env python
# coding=utf-8
import requests
from bs4 import BeautifulSoup

def get_city_list(url):
    web_data = requests.get(url)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'lxml')
    label = soup.select('div.foot_v2 > dl.link_dl > dd > a')
    cities = []
    cityName = []

    for var in range(0, len(label)):
        url = label[var].get('href')
        trueUrl = url if 'xiaozhu' in url else None
        if trueUrl:
            cities.append(trueUrl)
            cityName.append(label[var].text)

    return cities, cityName

if __name__ == "__main__":
    baseURL = 'http://www.xiaozhu.com'
    print(get_city_list(baseURL))
