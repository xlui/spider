#!/usr/bin/env python
# coding=utf-8
import requests, time, pymongo
from bs4 import BeautifulSoup
from getCityInfo import get_city_list
# 导入 getCityInfo 模块的 get_city_list 方法来获取该网站上热门城市的网址

def get_info(url, count):
# 获取短租房网页上的详细信息，并生成 list 返回
    web_data = requests.get(url)
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

def get_room_list_urls(pageURL, page):
# 获取pageURL 网页上的所有短租房的链接
    listUrl = []
    web_data = requests.get(pageURL)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'lxml')
    pagelist = soup.select('div.result_btm_con.lodgeunitname')
    for var in pagelist:
        listUrl.append(var.get('detailurl'))
    print('Page %d: get room list urls Done!' % (page))
    return listUrl

def get_page_info(startPage, endPage, baseURL, database):
# 获取一个城市的短租房网页上的所有信息并存入数据库
# 观察得到结论：热门城市的短租房信息总是13页，从p1--p13，startPage1，endPage14
    count = 1
    listUrls = []
    for var in range(startPage, endPage + 1):
        url = baseURL.format(var)
        listUrls += get_room_list_urls(url, var)
    for i in listUrls:
        #time.sleep(1)
        dataInfo = get_info(i, count)
        database.insert_one(dataInfo)
        count += 1
    print('one page data have beed insert into database!')

def main():
    baseUrl = 'http://www.xiaozhu.com/'
    client = pymongo.MongoClient('localhost', 27017)
    xiaozhu = client['xiaozhu']
    xiaozhu.drop_collection('Info_new')
    print("drop collection from database xiaozhu!")
    count = 0
    try:
        Info = xiaozhu['Info_new']

        cities, cityName = get_city_list(baseUrl)
        for var in cities:
            print('Get Info of city: %s, number: %d of total 24' % (cityName[count], count + 1))
            pageBaseUrl = var + 'search-duanzufang-p{}-0/'
            get_page_info(1, 13, pageBaseUrl, Info)
            count += 1
        print("All data has been insert into mongodb")
    except KeyboardInterrupt:
        pass
#        mydb = client.xiaozhu
#        mydb.drop_collection('Info_new')
#    client = pymongo.MongoClient('localhost', 27017)
#    mydb = client.xiaozhu
#    for info in mydb.Info.find({'price':{'gte':500}}):
#        print(info)

if __name__ == "__main__":
    main()
