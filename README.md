# Spider Web Project

A spider web project which get rental information from website [xiaozhu](http://www.xiaozhu.com), save those data into MonogoDB, and show them at a Django based web page.

<br>

## Current plan: [current.md](https://github.com/nxmup/spiderWebProject/blob/dev/current.md)

<br>

## Schedule:
Complete getting room urls of hot 24 citites, and successfully save them into MongoDB(About 7k data).   

Get Detail data of rental houses and save into database is the next step.

You can run the follow command to get rental room urls:  
`python App/save_url.py`

please make sure you have installed mongodb and opened it.

<br>

## Python Package Reuqirements:
> beautifulsoup4  
> Django  
> lxml  
> mongoengine  
> pymongo
> requests
> urllib3

You can install them through follow command:  
`pip install -r requirements.txt`

<br>

## Usage:
> Not complete, will not write this now.
