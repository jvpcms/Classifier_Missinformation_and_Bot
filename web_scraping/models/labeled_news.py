from dataclasses import dataclass
from datetime import datetime

from web_scraping.config.factory import get_config

from functools import partial
from nltk.tokenize import word_tokenize as nltk_word_tokenize
from nltk.corpus import stopwords as nltk_stopwords

from utils.time import time_struct_to_datetime

config = get_config()
portuguese_word_tokenize = partial(nltk_word_tokenize, language=config.envs.language)
portuguese_stopwords = set(nltk_stopwords.words(config.envs.language))


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


@dataclass
class LabeledNews:
    url: str
    title: str
    source_url: str
    label: bool
    date_published: datetime | None
    date_added: datetime

    @staticmethod
    def from_dict(d: dict) -> "LabeledNews":
        return LabeledNews(
            url=d["link"],
            title=d["title"],
            source_url=d["url_source"],
            label=d["label"],
            date_published=time_struct_to_datetime(d.get("published_parsed", None)),
            date_added=datetime.now(),
        )

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "title": self.title,
            "source_url": self.source_url,
            "label": self.label,
            "date_added": self.date_added.timestamp(),
            "date_published": (
                self.date_published.timestamp()
                if self.date_published is not None
                else None
            ),
        }

    def get_search_query(self) -> str:
        return f"{self.title} {self.source_url}"
