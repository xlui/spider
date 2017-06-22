# 爬虫Web项目

## 项目地址：[spiderWebProject](https://github.com/nxmup/spiderWebProject)

## 项目目前进度： [current.md](https://github.com/nxmup/spiderWebProject/blob/dev/current.md)

## 项目细节：

### 1. 项目构思：
> 写一个爬虫项目，爬取大量租房数据，利用Django将数据存放到网页上，在网页上添加数据分析等操作。

### 2. 依赖
> python-beautifulesoup4
>
> python-django
>
> python-lxml
>
> python-pymongo
>
> mongoengine(pip install)
>
> mongodb

### 3. 运行
> python getInfo.py
>
> 会将爬取的数据保存在本地数据库中，以便于 Django 网站的读取，后续可以把数据库直接保存在本地。
>
> 运行网站：
>
> cd webPage
>
> sudo systemctl start mongodb
>
> python manage.py runserver
>
> 打开浏览器，输入 127.0.0.1:8000 即可看到 Django 网站，同时也可以进行查询等操作。
