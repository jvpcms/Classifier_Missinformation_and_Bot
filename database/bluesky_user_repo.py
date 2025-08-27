from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
from models.bluesky_user_model import BlueSkyUser


class BlueSkyUserRepo:
    collection: Collection

    def __init__(self, db: Database):
        self.collection = db.bluesky_users
        self.collection.create_index("did", unique=True, name="did_index")

    def find(self) -> list[BlueSkyUser]:
        return [
            BlueSkyUser.from_db_entry(user)
            for user in self.collection.find({})
        ]

    def insert(self, user: BlueSkyUser) -> BlueSkyUser:
        self.collection.insert_one(user.to_dict())

        return user
