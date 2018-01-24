# coding:utf-8
# 测试 proxy 的连接
import requests

protocol = 'https'
ip, port = '139.209.107.110	80'.split()


proxies = {'{}'.format(protocol): '{}://{}:{}'.format(protocol, ip, port)}
url = 'http://bj.xiaozhu.com/fangzi/6937392816.html'
try:
    result = requests.get(url, proxies=proxies, timeout=1.5)
except requests.exceptions.Timeout:
    print('Timeout Failed!')
else:
    if result.status_code != 403:
        print('Success!')
        print(proxies)
    else:
        print('403 Failed!')
