from pymongo import MongoClient
from pymongo.synchronous.database import Database
from config.env_config import EnvConfig
from config.factory import get_config


class DatabasesFactory:
    reddit: Database

    def __init__(self, config: EnvConfig):
        CONNECTION_STRING = f"mongodb://{config.mongo_username}:{config.mongo_password}@localhost:27017/"
        print(CONNECTION_STRING)
        client = MongoClient(CONNECTION_STRING)

        self.reddit = client.reddit_data


databases = DatabasesFactory(get_config().envs)
