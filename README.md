# Spider Web Project

A spider web project which get rental information from website [xiaozhu(http://www.xiaozhu.com)](http://www.xiaozhu.com), save those data into MonogoDB, and show them at a Django based web page.

<br>

## Current plan: [current.md](https://github.com/nxmup/spiderWebProject/blob/dev/current.md)

<br>

## Now Complete

- get all city urls and save into database.
- get all city room urls from city urls in database and save them into database, also generate a table shows statistics.
- get all room data from room urls in database and save them into database.
- show statistical information in a Django driven web page.

<br>

## Schedule:

- [x] Complete getting room urls of hot 24 citites, and successfully save them into MongoDB(About 7k data).   

- [x] Get Detail data of rental houses and save into database is the next step.

You can run the follow command to get rental room urls:  
```bash
python App/save_url.py
```

Please make sure you have installed mongodb and opened it.

<br>

## Python Package Reuqirements:
> beautifulsoup4  
> Django  
> lxml  
> mongoengine  
> pymongo
> requests
> urllib3

You can install them through following command:  
```bash
pip install -r requirements.txt
```

<br>

## Usage:

Please make sure you have installed MongoDB and opened it.

**1. Get city-url corresponding relation**

```bash
python3 App/get_cities.py
```

this will get all city-url corresponding relation from a private link of the website, and save them into a table of database `xiaozhu` in MongoDB.

**2. Get all city room urls from the web site**

```
python3 App/save_url.py
```

the program will try to get city-url corresponding relation from a json format file if exist in folder `Data`, if not exist, will get them from the private mentioned above(feature: get the corresponding relation from MongoDB). And after get the relation, it will use a `for-loop` to get all the rental room urls and save into MongoDB.

**3. Get all rental room information**

```bash
python3 App/save_room_data.py
```

Please make sure you have runned the above two steps. This script will read `city-url` corresponding relation from MongoDB and get `city name`, then use the `city name` to query `city room urls` from collection `room_url` which created by script `save_url.py`.

After get all rental room's url of a city, the script will use a `for-loop` to get detail rental room's information and use a for-loop to save room information into MongoDB(feature: use multiprocess instread of for-loop).

**4. Show information in WebPage**

```bash
python WebPage/manage.py runserver
```

Open your browser and visit [http://localhost:8000](http://localhost:8000).

The rental room's information from MongoDB will show in different classify due to your choice.
