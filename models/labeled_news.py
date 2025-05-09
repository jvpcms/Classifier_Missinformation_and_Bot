from dataclasses import dataclass
from datetime import datetime

from config.envconfig import get_config

from functools import partial
from nltk.data import path as nltk_path
from nltk.tokenize import word_tokenize as nltk_word_tokenize
from nltk.corpus import stopwords as nltk_stopwords

from utils.time import time_struct_to_datetime

config = get_config()
nltk_path.append(config.envs.nltk_data_path)
portuguese_word_tokenize = partial(
    nltk_word_tokenize, language=config.envs.language
)
portuguese_stopwords = set(nltk_stopwords.words(config.envs.language))


@dataclass
class LabeledNews:
    url: str
    source_url: str
    title: str | None
    description: str | None
    claim_review: str | None
    review_body: str | None
    best_rating: int | None
    rating_value: int | None
    label: bool | None
    date_published: datetime | None
    date_added: datetime

    @staticmethod
    def from_dict(d: dict) -> "LabeledNews":
        return LabeledNews(
            url=d["link"],
            source_url=d["url_source"],
            title=d.get("title", None),
            description=d.get("description", None),
            claim_review=d.get("claim_review", None),
            review_body=d.get("review_body", None),
            best_rating=d.get("best_rating", None),
            rating_value=d.get("rating_value", None),
            label=d.get("label", None),
            date_published=time_struct_to_datetime(
                d.get("published_parsed", None)
            ),
            date_added=datetime.now(),
        )

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "source_url": self.source_url,
            "title": self.title,
            "description": self.description,
            "claim_review": self.claim_review,
            "review_body": self.review_body,
            "label": self.label,
            "date_added": self.date_added.timestamp(),
            "date_published": (
                self.date_published.timestamp()
                if self.date_published is not None
                else None
            ),
        }

    def get_search_query(self) -> list[str]:
        if self.description is None:
            return []

        return portuguese_word_tokenize(self.description)
