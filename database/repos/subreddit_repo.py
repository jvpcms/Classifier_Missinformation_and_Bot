from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
from social_media_api.models.subreddit_model import Subreddit


class SubredditRepo:
    collection: Collection

    def __init__(self, db: Database):
        self.collection = db.subreddits
        self.collection.create_index(
            "name", unique=True
        )  # use the acctual reddit name as pk

    def insert(self, subreddit: Subreddit) -> Subreddit:
        self.collection.insert_one(subreddit.to_dict())

        return subreddit
