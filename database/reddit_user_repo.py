from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
from models.reddit_user_model import RedditUser


class RedditUserRepo:
    collection: Collection

    def __init__(self, db: Database):
        self.collection = db.reddit_users
        self.collection.create_index("name", unique=True, name="name_index")

    def insert(self, user: RedditUser) -> RedditUser:
        self.collection.insert_one(user.to_dict())

        return user
