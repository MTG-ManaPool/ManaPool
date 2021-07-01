import pymongo
import json

config = json.load(open("config.json"))
SERVER_NAME = config["SERVER_NAME"]


class mongo:
    def __init__(self):
        # Set up database connection
        self.client = pymongo.MongoClient(SERVER_NAME)
        self.inventory = self.client["inventory"]
        self.cards = self.inventory["cards"]
        self.batch_limit = 1000 # Mongo caps batch size at 1000
