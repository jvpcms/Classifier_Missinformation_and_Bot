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
