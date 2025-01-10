from dataclasses import dataclass
from datetime import datetime


@dataclass
class LabeledNews:
    id: str
    url: str
    author: str
    date_published: datetime
    claim_reviewed: str
    review_body: str
    title: str
    rating_value: int
    best_rating: int
    alternative_name: bool
    date_added: datetime
