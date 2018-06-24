# global config here, includes data file paths, urls, user-agents and so on.
import os
import json


# paths
dir_name = os.path.dirname(os.path.abspath(__file__))
data_dir_name = os.path.join(os.path.split(dir_name)[0], 'data')

city_json_file = os.path.join(data_dir_name, 'cities.json')
url_json_file = os.path.join(data_dir_name, 'urls.json')
proxies_json_file = os.path.join(data_dir_name, 'proxies.json')


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
headers_count = len(headers)


# MySQL
host = "127.0.0.1"
port = 33306
database = 'xiaozhu'
user = 'xiaozhu'
passwd = 'xiaozhu'
