#!/usr/bin/env python
# coding=utf-8
# 使用 BeautifulSoup 的示例

# 我们在写 CSS 时，标签名不加任何修饰，类名前加点，id名前加 #，
# 在这里我们也可以利用类似的方法来筛选元素，用到的方法是 soup.select()，返回类型是 list
# 1. 通过标签名查找：   soup.select('title')
# 2. 通过类名查找：     soup.select('.sister')
# 3. 通过 id 名查找：   soup.select('#link1')
# 4. 组合查找：
#        类组合：      soup.select('.member_pic .member_ico1')
#        子标签组合：   soup.select("head > title")
# 5. 属性查找：         soup.select('a[class="sister"]')
import requests
from bs4 import BeautifulSoup

url = 'http://bj.xiaozhu.com/fangzi/6937392816.html'

web_data = requests.get(url)
web_data.encoding = 'utf-8'
soup = BeautifulSoup(web_data.text, 'lxml')

title = soup.select('h4 em')[0].text
gender = '女' if soup.select('.member_ico1') else '男'

print('链接：', url)
print('标题: ', title)
print('性别: ', gender)
