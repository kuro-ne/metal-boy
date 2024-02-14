import datetime
import os
import sqlite3
from typing import Optional

from pymongo.mongo_client import MongoClient

from w3gg import get_leaderboard

MAX_TARGET_WXP = int(float(os.getenv("MAX_TARGET_WXP", "7000")))

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
        self.mongo_uri = os.getenv("MONGO_URI", None)
        if not self.mongo_uri:
            raise Exception('MONGO_URI is not set')

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

    def get_active_referral_code(self) -> Optional[str]:
        # get data from "referral" collection
        # filter "active" is True
        # return "referral_code"
        db = self.mongo_client['account']
        collection = db['referral']
        datas = collection.find({"active": True})

        for data in datas:
            id = data.get("id", None)
            l = get_leaderboard(id)
            wxp = 0
            referral_code = None
            if l:
                wxp = l.get("wxp", 0)
            if wxp < MAX_TARGET_WXP :
                referral_code = data.get("referral_code", None)

            if referral_code:
                return referral_code

        return None

