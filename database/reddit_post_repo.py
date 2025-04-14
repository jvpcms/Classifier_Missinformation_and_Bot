from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
from models.reddit_post_model import RedditPost


class RedditPostRepo:
    collection: Collection

    def __init__(self, db: Database):
        self.collection = db.reddit_posts
        self.collection.create_index(
            "name", unique=True
        )  # use the acctual reddit name as pk

    def insert(self, post: RedditPost) -> RedditPost:
        self.collection.insert_one(post.to_dict())

        return post
