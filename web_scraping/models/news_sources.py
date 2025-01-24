from dataclasses import dataclass
from typing import Literal


@dataclass
class NewsSource:
    feed_url: str
    base_url: str
    country: str
    source_type: Literal["virtual_media", "checking_agency"]
