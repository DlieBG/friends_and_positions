from pymongo import MongoClient
from pymongo.collection import Collection
import os


class FAPDatabase(object):
    def __init__(self, collection_name: str) -> None:
        self.client = MongoClient(os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017'))
        self.db = self.client.get_database('friends_and_positions')
        self.collection = self.db.get_collection(collection_name)
     
    def __enter__(self) -> Collection:
        return self.collection
 
    def __exit__(self, *args) -> None:
        self.client.close()
