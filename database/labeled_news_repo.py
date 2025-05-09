from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
from models.labeled_news import LabeledNews


class LabeledNewsRepo:
    collection: Collection

    def __init__(self, db: Database):
        self.collection = db.labeled_news

    def insert(self, news: LabeledNews) -> LabeledNews:
        self.collection.insert_one(news.to_dict())

        return news

    def select_all(self) -> list[LabeledNews]:
        return [LabeledNews.from_dict(news) for news in self.collection.find()]
