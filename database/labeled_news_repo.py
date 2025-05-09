from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
from models.labeled_news import LabeledNews


class LabeledNewsRepo:
    collection: Collection

    def __init__(self, db: Database):
        self.collection = db.labeled_news
        self.collection.create_index("link", unique=True, name="link_index")

    def insert(self, news: LabeledNews) -> LabeledNews:
        """Insert a new LabeledNews document in the collection"""

        self.collection.insert_one(news.to_dict())

        return news

    def find_all(self) -> list[LabeledNews]:
        """Find all LabeledNews documents in the collection"""

        return [LabeledNews.from_dict(news) for news in self.collection.find()]
