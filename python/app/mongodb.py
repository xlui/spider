# 数据库模块，封装 MongoDB 的操作
import pymongo

from config.config import mongo_host, mongo_port, mongo_db


class MongoDB:
    def __init__(self, host=mongo_host, port=mongo_port) -> None:
        super().__init__()
        self.client = pymongo.MongoClient(host=host, port=port)
        self.db = self.client[mongo_db]

    def save(self, collection, **kwargs):
        db_collection = self.db[collection]
        return db_collection.insert_one({**kwargs})

    def drop(self, collection):
        res = self.db.drop_collection(collection)
        if res.get('ok'):
            print('Successfully drop collection `{}`'.format(collection))
            return True
        else:
            print('Failed to drop collection `{}`'.format(collection))
            return False

    def query(self, collection, **kwargs):
        db_collection = self.db[collection]
        return list(db_collection.find({**kwargs}))

    def print(self, collection):
        print('\nData in collection `{}`:'.format(collection))
        dbc = self.db[collection]
        docs = dbc.find()
        for doc in docs:
            print(doc)
        print('Total:', docs.count(), 'documents.')

    def close(self):
        self.client.close()


if __name__ == '__main__':
    import threading
    db = MongoDB()

    data_count = 59
    thread_count = 10
    threads = []
    separate = data_count // thread_count
    collection = 'test'

    total_list = list(range(data_count))
    db.drop(collection)


    def save_db(from_, to_):
        sub_list = total_list[from_:to_]
        for i in sub_list:
            db.save(collection, url_count=i, url='https://www.baidu.com/?page={}'.format(i))


    # start multithreading
    print('Start writing data into mongodb....')
    for index in range(thread_count):
        if index == (thread_count - 1):
            thread = threading.Thread(target=save_db, args=(index * separate, data_count))
        else:
            thread = threading.Thread(target=save_db, args=(index * separate, index * separate + separate))
        thread.start()
        threads.append(thread)
    [thread.join() for thread in threads]

    print("All threads' work Done!")

    db.print(collection)
    db.close()
