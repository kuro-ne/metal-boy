import datetime
import sqlite3

from pymongo.mongo_client import MongoClient


class DB:
    def __init__(self):
        self.mongo_client = None
        self.mongo_uri = None
        self.cursor = None
        self.sqlite_connection = None
        self.DB_TYPE = 'mongodb'  # sqlite, mongodb

        switcher = {
            'sqlite': self.init_sqlite,
            'mongodb': self.init_mongodb
        }

        switcher.get(self.DB_TYPE)()

    def init_mongodb(self):
        self.mongo_uri = 'mongodb+srv://xloader96:makankue22@cluster0.vzsqu0s.mongodb.net/?retryWrites=true&w=majority'
        self.mongo_client = MongoClient(self.mongo_uri)
        # Send a ping to confirm a successful connection
        try:
            self.mongo_client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def init_sqlite(self):
        # save to sqlite
        self.sqlite_connection = sqlite3.connect('db/account.sqlite')
        self.cursor = self.sqlite_connection.cursor()
        print('DB Init')
        query = 'select sqlite_version();'
        self.cursor.execute(query)
        # Fetch and output result
        result = self.cursor.fetchall()
        print('SQLite Version is {}'.format(result))

    def __del__(self):
        if self.DB_TYPE == 'sqlite':
            if self.cursor:
                self.cursor.close()
            if self.sqlite_connection:
                self.sqlite_connection.close()
        elif self.DB_TYPE == 'mongodb':
            if self.mongo_client:
                self.mongo_client.close()

    def insert(self, data: dict):
        switcher = {
            'sqlite': self.insert_sqlite,
            'mongodb': self.insert_mongodb
        }
        switcher.get(self.DB_TYPE)(data)
        print('Insert Success')

    def insert_mongodb(self, data: dict):
        db = self.mongo_client['account']
        collection = db['account']
        data['created_at'] = datetime.datetime.now()
        collection.insert_one(data)

    def insert_sqlite(self, data: dict):
        payload: tuple = (
            data.get("name", None),
            data.get("email", None),
            data.get("password", None),
            data.get("referral_code", None),
            data.get("registered", True),
            data.get("verified", True),
            data.get("created_at", datetime.datetime.now())
        )

        query = '''
            insert into account (
                name,
                email,
                password,
                referral_code,
                registered,
                verified,
                created_at
            ) values (?, ?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(query, payload)
        self.sqlite_connection.commit()
