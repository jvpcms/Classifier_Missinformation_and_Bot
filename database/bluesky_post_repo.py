from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
from models.bluesky_post_model import BlueSkyPost
from pymongo import ReturnDocument
from typing import Union


class BlueSkyPostRepo:
    collection: Collection

    def __init__(self, db: Database):
        self.collection = db.bluesky_posts
        self.collection.create_index("uri", unique=True, name="uri_index")

    def insert(self, post: BlueSkyPost) -> BlueSkyPost:
        self.collection.insert_one(post.to_dict())
        return post

    def find(self) -> list[BlueSkyPost]:
        return [
            BlueSkyPost.from_db_entry(post)
            for post in self.collection.find({})
        ]

    def find_by_news_link(self, news_link: str) -> list[BlueSkyPost]:
        return [
            BlueSkyPost.from_db_entry(post)
            for post in self.collection.find({"news_link": news_link})
        ]

    def update_by_uri(
        self, uri: str, updates: dict, upsert: bool = False
    ) -> Union[BlueSkyPost, None]:
        # Never try to update _id
        updates = {k: v for k, v in updates.items() if k != "_id"}
        doc = self.collection.find_one_and_update(
            {"uri": uri},
            {"$set": updates, "$setOnInsert": {"uri": uri}},
            upsert=upsert,
            return_document=ReturnDocument.AFTER,
        )
        return BlueSkyPost.from_db_entry(doc) if doc else None
