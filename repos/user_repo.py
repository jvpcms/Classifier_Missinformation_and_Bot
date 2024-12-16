from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
from models.user_model import User


class UserRepo:
    collection: Collection

    def __init__(self, db: Database):
        self.collection = db.users
        self.collection.create_index(
            "name", unique=True
        )  # use the acctual reddit name as pk

    def insert(self, user: User) -> User:
        self.collection.insert_one(user.to_dict())

        return user
