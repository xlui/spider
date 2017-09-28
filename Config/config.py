# save config variables here!
import os
import json

# dir name and json path
dir_name = os.path.dirname(os.path.abspath(__file__))
city_json_file = os.path.join(dir_name, 'cities.json')
proxies_json_file = os.path.join(dir_name, 'proxies.json')


# url
root_url = 'http://www.xiaozhu.com'


# header
headers = [
    {'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 '
                   '(KHTML, like Gecko) Version/5.1 Safari/534.50'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 '
                   '(KHTML, like Gecko) Version/5.1 Safari/534.50'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; '
                   '.NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko'}
]
headers_length = len(headers)
# proxy
with open(proxies_json_file, 'r') as file:
    proxies = json.load(file)
proxies = [{"http":"http://{}".format(proxy)} for proxy in proxies]
proxies_length = len(proxies)
# print(proxies)


# mongodb
db_url = 'localhost'
db_port = 27017
database = 'xiaozhu'
room_url_collection = 'room_url'
room_data_collection = 'room_data'
sample_collection = 'test'
