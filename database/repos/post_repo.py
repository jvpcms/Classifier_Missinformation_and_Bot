from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
from reddit_api.models.post_model import Post


class PostRepo:
    collection: Collection

    def __init__(self, db: Database):
        self.collection = db.posts
        self.collection.create_index(
            "name", unique=True
        )  # use the acctual reddit name as pk

    def insert(self, post: Post) -> Post:
        self.collection.insert_one(post.to_dict())

        return post
