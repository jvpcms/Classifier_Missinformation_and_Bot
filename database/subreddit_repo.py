from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
from models.subreddit_model import Subreddit


class SubredditRepo:
    collection: Collection

    def __init__(self, db: Database):
        self.collection = db.subreddits
        self.collection.create_index("name", unique=True)

    def insert(self, subreddit: Subreddit) -> Subreddit:
        self.collection.insert_one(subreddit.to_dict())

        return subreddit
