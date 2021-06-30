import pymongo
import json

config = json.load(open('config.json'))
SERVER_NAME = config['SERVER_NAME']
USER = config['USER']
PASSWORD = config['PASSWORD']


class mongo:
    def __init__(self):
        # Set up database connection
        self.client = pymongo.MongoClient(
            SERVER_NAME,
            username=USER,
            password=PASSWORD,
            authSource='collection_name'
        )
        self.db_collection = self.client.collection_name
        self.batch_limit = 1000 # Mongo caps batch size at 1000
