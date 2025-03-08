from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class NewsSource:
    feed_url: str
    base_url: str
    country: str
    source_type: Literal["virtual_media", "checking_agency"]
    feed_url_true_news: Optional[str] = None
    feed_url_fake_news: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "feed_url": self.feed_url,
            "base_url": self.base_url,
            "country": self.country,
            "source_type": self.source_type,
            "feed_url_true_news": self.feed_url_true_news,
            "feed_url_fake_news": self.feed_url_fake_news,
        }

    @staticmethod
    def from_dict(data: dict) -> "NewsSource":
        return NewsSource(
            feed_url=data["feed_url"],
            base_url=data["base_url"],
            country=data["country"],
            source_type=data["source_type"],
            feed_url_true_news=data.get("feed_url_true_news"),
            feed_url_fake_news=data.get("feed_url_fake_news"),
        )
