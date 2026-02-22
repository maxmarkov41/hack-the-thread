# import os
import time
# from dotenv import load_dotenv

# load_dotenv()

# uri = os.getenv('connection_string')

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class MNG:
    def __init__(self, uri, db_name, collection_name):
        self.uri = uri
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db_name = db_name
        self.collection_name = collection_name
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def insert(self,data):
        data['_id'] = time.time_ns()
        result = self.collection.insert_one(data)
        print("Successfully saved data with ID:", result.inserted_id)

    def get(self):
        cursor = self.collection.find({}) # getting all documents
        return list(cursor)
    
    def get_by_tag(self, tag:str):
        cursor = self.collection.find({'processed_response.autotag':tag})
        return list(cursor)
    
    def get_by_time(self, start, end=None):
        if not end:
            cursor = self.collection.find({'_id':{"$gt":start}})
        else:
            cursor = self.collection.find({'_id': {"$gt": start, "$lt": end}})
        return list(cursor)