from dataclasses import dataclass
from datetime import datetime
import time


# title
# title_detail
#      type
#      language
#      base
#      value
# summary
# summary_detail
#      type
#      language
#      base
#      value
# links
# link
# id
# guidislink
# tags
# authors
# author
# author_detail
#      name
# published
# published_parsed


def time_struct_to_datetime(ts: time.struct_time | None) -> datetime | None:
    """Convert time.struct_time to datetime"""
    if ts is None:
        return None

    return datetime.fromtimestamp(time.mktime(ts))


@dataclass
class LabeledNews:
    id: str
    url: str
    url_source: str
    title: str
    author: str
    label: bool
    date_published: datetime | None
    date_added: datetime

    @staticmethod
    def from_dict(d: dict) -> "LabeledNews":
        return LabeledNews(
            id=d["id"],
            url=d["link"],
            url_source=d["url_source"],
            title=d["title"],
            author=d.get("author", ""),
            label=d["label"],
            date_published=time_struct_to_datetime(d.get("published_parsed", None)),
            date_added=datetime.now(),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "url": self.url,
            "url_source": self.url_source,
            "title": self.title,
            "author": self.author,
            "label": self.label,
            "date_added": self.date_added.timestamp(),
            "date_published": (
                self.date_published.timestamp()
                if self.date_published is not None
                else None
            ),
        }
