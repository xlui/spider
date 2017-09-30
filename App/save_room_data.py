# get room link from MongoDB and get the detail data them save to another collection in MongoDB
from contextlib import closing
from multiprocessing import Pool
from App.mongodb import MongoDB
from App.get_room_data import GetRoomData
from Config.config import city_info_collection, room_url_collection, room_data_collection


def main(city, thread_count=16):
    with closing(MongoDB()) as db:
        urls = db.query(room_url_collection, city_name=city)
        print('{} get room url of city [{}] from database'.format('Successfully' if urls else 'Failed to', city))
        # now, get all room urls of a city from database
    room_url_list = [url.get('room_url') for url in urls]
    room_data_list = []
    get_room_data = GetRoomData()

    for room_url in room_url_list:
        room_data_list.append(get_room_data.get(room_url))

    with closing(MongoDB()) as db:
        for room_data in room_data_list:
            db.save(room_data_collection, **room_data)
    print('All data has been inserted into database.')


if __name__ == '__main__':
    from contextlib import closing
    with closing(MongoDB()) as db:
        db.drop(room_data_collection)
        cities = db.query(city_info_collection)
    [main(city.get('city')) for city in cities]
