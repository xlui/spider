#!/usr/bin/env python
# coding:utf-8
# use crossincode's api to get proxy ip
import os
import json
import requests


def update(file, save=False):
    url = 'http://lab.crossincode.com/proxy/get/?num=5&head=http'

    data = requests.get(url)
    data.encoding = 'utf-8'
    data_dict = eval(data.text)

    proxies = [proxies.get('http') for proxies in data_dict.get('proxies')]

    if save:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(proxies, f)

    print('proxies:\n', proxies)


def test(file, save=False):
    valid = []
    with open(file, 'r', encoding='utf-8') as f:
        proxies = json.load(f)
    os.remove(file)
    use_proxies = [{"http": "http://{}".format(proxy)} for proxy in proxies]
    for proxy in use_proxies:
        try:
            requests.get('http://bj.xiaozhu.com/fangzi/6937392816.html', proxies=proxy, timeout=1.5)
            # print(web_data.text)
            # print(proxy)
        except Exception as e:
            print(e)
        else:
            valid.append(proxy)

    if save:
        with open(proxies_json_file, 'w', encoding='utf-8') as f:
            json.dump(valid, f)


if __name__ == '__main__':
    from Config.config import proxies_json_file
    save_file = 'tmp.json'
    update(file=save_file, save=True)
    test(save_file, save=False)
