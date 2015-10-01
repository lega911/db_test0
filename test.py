
import sys
import uuid
import time
import random

sys.path.append('/app/mongo-python-driver')
sys.path.append('/app/pyorient_lib')

import bson
import pymongo
import pyorient

db = pymongo.MongoClient('tt_mongo').bb
client = pyorient.OrientDB("tt_orient", 2424)


def mongo_fill(count):
    parents = []
    null = bson.ObjectId()
    for i in range(count):
        name = str(uuid.uuid4())
        doc = {'name': name, 'parent': null}
        db.user.insert(doc, w=0)
        if random.random() < 0.01:
            parents.append(doc['_id'])

    # set parents
    print('parents', len(parents))
    for doc in db.user.find({}, {'_id': 1}).sort('_id'):
        parent_id = random.choice(parents)
        db.user.update({'_id': doc['_id']}, {'$set': {'parent': parent_id}}, w=0)

    db.user.ensure_index('name')


def orient_fill():
    client.connect("root", "0r13ntDB")

    if client.db_exists('bb'):
        client.db_drop('bb')
    client.db_create('bb', pyorient.DB_TYPE_GRAPH)

    client.db_open('bb', "root", "0r13ntDB")
    client.command('create class User extends V')
    client.command('create property User.name string')
    client.command('create property User.parent link')
    client.command('create index User.name NOTUNIQUE')

    # fill
    for i, d in enumerate(db.user.find({}, {'name': 1}).sort('_id')):
        if not i % 1000:
            print(i)

        client.command('create vertex User set name="{}"'.format(d['name']))

    # connect to parents
    for i, d in enumerate(db.user.find().sort('_id')):
        if not i % 1000:
            print(i)

        parent = db.user.find_one(d['parent'])
        assert parent

        q = "update User set parent=(select from User where name='{}') where name='{}'".format(parent['name'], d['name'])
        client.command(q)


def mongo_select():

    def one(filter):
        result = list(db.user.find({'name': {'$gt': filter}}).sort('name').limit(100))
        parents = set()
        for d in result:
            parents.add(d['parent'])

        parents = list(db.user.find({'_id': {'$in': list(parents)}}))
        assert len(result) == 100

    time.sleep(2)
    start = time.time()
    for i in range(100):
        one(str(i))
    print('duration', time.time()-start)


def orient_select():
    client.db_open('bb', "root", "0r13ntDB")

    def one(filter):
        q = 'select name, parent.name from User where name > "{}" order by name limit 100'.format(filter)
        result = client.query(q)
        assert len(result) == 100

    time.sleep(2)
    start = time.time()
    for i in range(100):
        one(str(i))
    print('duration', time.time()-start)


if sys.argv[1] == 'mongo_fill':
    mongo_fill(int(sys.argv[2]))
else:
    globals()[sys.argv[1]]()
