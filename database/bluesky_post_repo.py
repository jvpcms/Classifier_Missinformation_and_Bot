from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
from models.bluesky_post_model import BlueSkyPost


class BlueSkyPostRepo:
    collection: Collection

    def __init__(self, db: Database):
        self.collection = db.bluesky_posts
        self.collection.create_index("uri", unique=True, name="uri_index")

    def insert(self, post: BlueSkyPost) -> BlueSkyPost:
        self.collection.insert_one(post.to_dict())

        return post
