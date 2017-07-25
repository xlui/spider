#!/usr/bin/env python
# coding=utf-8
# defined method to get city's link from webset www.xiaozhu.com
import requests
from bs4 import BeautifulSoup


def get_city_url(url):
    cities = []
    cityName = []

    web_data = requests.get(url)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'lxml')

    label = soup.select('div.foot_v2 > dl.link_dl > dd > a')
    # get city links from www.xiaozhu.com

    for var in range(0, len(label)):
        # get single city link
        url = label[var].get('href')
        trueUrl = url if 'xiaozhu' in url else None
        # test link is true or not, because there are AD links also
        if trueUrl:
            cities.append(trueUrl)
            cityName.append(label[var].text)

    return cities, cityName


if __name__ == "__main__":
    baseURL = 'http://www.xiaozhu.com'
    print(get_city_url(baseURL))
