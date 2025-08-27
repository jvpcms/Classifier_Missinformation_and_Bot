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

    def find(self) -> list[BlueSkyPost]:
        entries = self.collection.find()
        retured_posts = []

        for entry in entries:
            print(entry)
            retured_posts.append(BlueSkyPost.from_db_entry(entry))

        return retured_posts

    def find_by_news_link(self, news_link: str) -> list[BlueSkyPost]:
        return [
            BlueSkyPost.from_db_entry(post)
            for post in self.collection.find({"news_link": news_link}) 
        ]
