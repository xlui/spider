#!/usr/bin/env python
# coding:utf-8
import threading
from get_cities import GetCities
from save_to_database import Save
import get_city_room_list

get_cities = GetCities()
save = Save()
cities = get_cities.get()
cities = cities[0:1]
for city in cities:
    get_city_room_url_list = get_city_room_list.GetCityRoomUrlList(city.get('url'))
    room_url_list = get_city_room_url_list.get()
    save.drop_url()

    list_count = len(room_url_list)
    thread_count = 20
    threads = []
    separate = list_count // thread_count
    city_name = city.get('name')

    def save_to_db(from_, to_):
        sub_list = room_url_list[from_:to_]
        for room_url in sub_list:
            save.save_url(city_name, room_url)

    for thread_index in range(thread_count):
        if thread_index == (thread_count - 1):
            thread = threading.Thread(target=save_to_db, args=(thread_index * separate, list_count))
        else:
            thread = threading.Thread(target=save_to_db, args=(thread_index * separate, thread_index * separate + separate))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    print('Total: {}'.format(len(room_url_list)))
    print('All room url of city', city_name, 'has been saved into database!')
