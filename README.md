# Spider Web Project

A spider web project which snatch at rental information from [xiaozhu](http://www.xiaozhu.com), save into MonogoDB, and show them at a Django based web page.

### current plan: [current.md](https://github.com/nxmup/spiderWebProject/blob/dev/current.md)

<br>

#### Dependencies: 
> Mongo Database(use package manager to install)
> 
> python-requests  
> python-pymongo  
> python-beautifulesoup4  
> python-lxml  
> python-django  
> mongoengine(use pip to install)  


#### Usage: 
get rental information, and save into MongoDB: 
```bash
$ sudo systemctl start mongodb
$ cd spiderWebProject/
$ python getInfo.py
```

run Django: 
```bash
$ cd webPage
$ python manage.py runserver
```

open you browser, and visit [127.0.0.1:8000](127.0.0.1:8000), you will see data from MongoDB in a simple web page.  
Also, you can choose different information to show use the button.
