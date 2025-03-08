from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
from web_scraping.models.news_sources import NewsSource


class NewsSourcesRepo:
    collection: Collection

    def __init__(self, db: Database):
        self.collection = db.news_sources

    def insert(self, source: NewsSource) -> NewsSource:
        """Insert a new NewsSource document in the collection"""

        self.collection.insert_one(source.to_dict())
        self.collection.create_index("base_url", unique=True)  # use base_url as pk

        return source

    def find_all(self) -> list[NewsSource]:
        """Find all NewsSource documents in the collection"""

        return [NewsSource.from_dict(source) for source in self.collection.find()]

    def find_by_base_url(self, base_url: str) -> NewsSource | None:
        """Find a NewsSource document by its base_url"""

        source = self.collection.find_one({"base_url": base_url})
        return NewsSource.from_dict(source) if source else None
