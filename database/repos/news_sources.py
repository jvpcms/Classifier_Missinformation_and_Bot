from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
from web_scraping.models.news_sources import NewsSource


class NewsSourcesRepo:
    collection: Collection

    def __init__(self, db: Database):
        self.collection = db.news_sources

    def insert(self, source: NewsSource) -> NewsSource:
        self.collection.insert_one(source.to_dict())

        return source
