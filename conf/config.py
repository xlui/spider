# save config variables here!

# url
root_url = 'http://www.xiaozhu.com'


# spider
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
}

proxy_ip = ['113.234.110.98']
proxy_port = ['80']
proxies = {}
# proxies = {'http': 'http://{}:{}'.format(proxy_ip.pop(), proxy_port.pop())}
# print(proxies)

# mongodb
database = 'xiaozhu'
room_url_collection = 'room_url'
room_data_collection = 'room_data'
