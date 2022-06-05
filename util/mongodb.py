from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database
from uuid import uuid4
from urllib.parse import quote_plus
from bson import ObjectId


class MongoDB:
    def __init__(self, Env: dict):
        self.Env = Env
        self.conn = None
        self.db = None
        self.collection = None

    def generateKey(self, prefix: str = 'biblia-api') -> str:
        return ''.join((prefix, uuid4().hex))

    def getDB(self) -> Database:
        if self.conn is None:
            self.conn = self.connection()

        return self.conn['biblia-api']

    def getCollection(self, name: str) -> Collection:
        if self.conn is None:
            self.conn = self.connection()

        if self.db is None:
            self.db = self.getDB()

        self.collection = self.db[name]

        return self.collection

    def findOne(self, filter: dict, collection: str = 'biblia') -> dict:
        if self.conn is None:
            self.conn = self.connection()

        self.collection = self.getCollection(name=collection)

        result = self.collection.find_one(filter=filter)

        if result:
            n_values = {}
            for key in result:
                if type(result[key]) != str:
                    result[key] = str(result[key])
                n_values.update({key: result[key]})
            return n_values
        return {}

    def findAll(self, filter: dict, collection: str = 'biblia') -> Cursor:
        if self.conn is None:
            self.conn = self.connection()

        self.collection = self.getCollection(name=collection)

        return self.collection.find(filter=filter)

    def set(self, _id: str = '', uid: str = '', data: dict = None, collection: str = 'biblia', prefix: str = '') -> dict:
        if not data:
            return {}

        if self.conn is None:
            self.conn = self.connection()

        self.collection = self.getCollection(name=collection)

        data['uid'] = uid if uid else self.generateKey(prefix=prefix)

        _get = {}

        if _id:
            _get = self.findOne(filter={'_id': ObjectId(_id)})

        if uid and not _id:
            _get = self.findOne(filter={'uid': uid})

        if not _get:
            insert = self.collection.insert_one(
                document=data
            )

            if type(data.get('_id')) == ObjectId:
                data['_id'] = ObjectId(data['_id']).__str__()

            if self.collection.count_documents(filter={'_id': insert.inserted_id}):
                result = {'insert': 1, 'values': data}
            else:
                result = {'insert': 0, 'values': {}}
        else:
            if type(_get.get('_id')) != ObjectId:
                _get['_id'] = ObjectId(_get['_id'])

            n_data = _get
            n_data.update(data)

            update = self.collection.update_one(
                filter={'_id': _get.get('_id')},
                update={"$set": n_data},
                upsert=True
            )

            if type(n_data.get('_id')) == ObjectId:
                n_data['_id'] = ObjectId(n_data['_id']).__str__()

            if update.modified_count:
                result = {'update': 1, 'values': n_data}
            else:
                result = {'update': 0, 'values': {}}

        return result

    def connection(self) -> MongoClient:
        if self.Env.get('MONGODB_PASSWORD'):
            uri = "mongodb://%s:%s@%s" % (
                quote_plus(self.Env.get('MONGODB_USERNAME')), quote_plus(self.Env.get('MONGODB_PASSWORD')),
                ':'.join((self.Env.get('MONGODB_HOST'), self.Env.get('MONGODB_PORT'))))
        else:
            uri = "mongodb://%s" % (':'.join((self.Env.get('MONGODB_HOST'), self.Env.get('MONGODB_PORT'))))

        self.conn = MongoClient(uri)

        return self.conn

    def close(self) -> bool:
        if self.conn is None:
            return False

        self.conn.close()
        self.conn = None

        return True
