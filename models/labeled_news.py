from dataclasses import dataclass
from datetime import datetime

from utils.time import time_struct_to_datetime

from utils.search_queries import get_custom_stopwords, portuguese_word_tokenize


@dataclass
class LabeledNews:
    link: str
    source_url: str
    title: str | None
    description: str | None
    claim_review: str | None
    review_body: str | None
    best_rating: int | None
    rating_value: int | None
    label: bool | None
    date_published: datetime | None
    date_added: datetime | None

    @staticmethod
    def from_dict(d: dict) -> "LabeledNews":
        return LabeledNews(
            link=d["link"],
            source_url=d["source_url"],
            title=d.get("title", None),
            description=d.get("description", None),
            claim_review=d.get("claim_review", None),
            review_body=d.get("review_body", None),
            best_rating=d.get("best_rating", None),
            rating_value=d.get("rating_value", None),
            label=d.get("label", None),
            date_published=time_struct_to_datetime(d.get("published_parsed", None)),
            date_added=datetime.now(),
        )

    @staticmethod
    def from_db_entry(entry: dict) -> "LabeledNews":
        return LabeledNews(
            link=entry["link"],
            source_url=entry["source_url"],
            title=entry.get("title", None),
            description=entry.get("description", None),
            claim_review=entry.get("claim_review", None),
            review_body=entry.get("review_body", None),
            best_rating=entry.get("best_rating", None),
            rating_value=entry.get("rating_value", None),
            label=entry.get("label", None),
            date_published=(
                datetime.fromtimestamp(entry["date_published"])
                if entry.get("date_published") is not None
                else None
            ),
            date_added=(
                datetime.fromtimestamp(entry["date_added"])
                if entry.get("date_added") is not None
                else None
            ),
        )

    def to_dict(self) -> dict:
        return {
            "link": self.link,
            "source_url": self.source_url,
            "title": self.title,
            "description": self.description,
            "claim_review": self.claim_review,
            "review_body": self.review_body,
            "label": self.label,
            "date_added": (
                self.date_added.timestamp() if self.date_added is not None else None
            ),
            "date_published": (
                self.date_published.timestamp()
                if self.date_published is not None
                else None
            ),
        }

    def get_search_query(self) -> str:
        if self.description is None:
            return ""

        query = portuguese_word_tokenize(self.description)
        custom_stopwords = get_custom_stopwords()

        return " ".join(list(filter(lambda x: x not in custom_stopwords, query)))
