#!/usr/bin/env python
# coding:utf-8
from App.get_city_room_url_list import GetCityRoomUrlList
from App.get_cities import GetCities
from App.mongodb import MongoDB
from Config.config import room_url_collection


def get_list_and_save(city_):
    get_city_room_url_list = GetCityRoomUrlList(city_.get('url'))

    # sleep to avoid being blocked -- in Multi Processes Case
    # sleep(randint(0, 20))
    room_url_list = get_city_room_url_list.get()

    database = MongoDB()

    list_count = len(room_url_list)

    city_name = city_.get('name')

    [database.save(room_url_collection, city_name=city_name, room_url=room_url) for room_url in room_url_list]

    database.save(collection='Overview', city_name=city_name, total_urls=list_count)

    database.close()

    print('Total: {} urls'.format(list_count))
    global count
    print('All room url of city {city} (count {current}/{total}) has been saved into database!'.format(
        city=city_name,
        current=count,
        total=total_count
    ))
    count += 1


if __name__ == '__main__':
    from contextlib import closing
    with closing(MongoDB()) as db:
        db.drop(room_url_collection)
        db.drop(collection='Overview')

    cities = GetCities().get()
    count = 1
    total_count = len(cities)
    # pool = Pool(24)
    # for city in cities:
    #     pool.apply_async(get_list_and_save, args=(city, ))
    # pool.close()
    # pool.join()
    # print('All subprocesses done.')
    [get_list_and_save(city) for city in cities]
