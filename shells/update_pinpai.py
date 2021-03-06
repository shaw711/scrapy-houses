# coding:utf-8

import pymongo
from bson.objectid import ObjectId
import datetime
from multiprocessing import Pool
# async def log(message):
client = pymongo.MongoClient('mongodb://10.6.52.147:27017')
collections = [
        "house_beijing",
        "house_chengdu",
        "house_chongqing",
        "house_guangzhou",
        "house_hangzhou",
        "house_nanjing",
        "house_shanghai",
        "house_suzhou",
        "house_tianjin",
        "house_wuhan",
        "house_xian",
        "house_zhengzhou"
    ]


def update_data(db,col):
    collection = client[db][col]
    for d in collection.find({'$or':[{'source_from':'pinpai58'},{'source_from':'beike'}]}, no_cursor_timeout=True):
        up = dict()
        try:
            if d['source_from'] == 'pinpai58' and d.get('apartment', '') == '':
                if d.get('rent_type') != 3:
                    up['apartment'] = d['title'].split(' ')[1]
                else:
                    up['apartment'] = d['title']

            if d['source_from'] == 'beike' and d.get('apartment', '') == '':
                up['apartment'] = d['brand']
        except Exception:
            print(d['title'])
            pass
        print(d,up)
        try:

            collection.update_one({'_id': ObjectId(d['_id'])}, {'$set': up}, upsert=True)
        except Exception as e:
            print(e)
    client.close()

def update_brand(db,col):
    collection = client[db][col]
    collection.update_many({'source_from':'ziroom'},{'$set': {'brand':'自如公寓'}})

def update_brand_batch():
    for col in collections:
        print(col)
        update_brand('house',col)

def update_collections_uniqe_keys():
    p = Pool(len(collections))
    for col in collections:
        p.apply(update_data, ('house', col))
    p.close()
    p.join()

update_brand_batch()    