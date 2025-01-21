from abc import ABC
from feedparser import parse
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from newspaper import Article
from typing import Union

from web_scraping.news_sources.news_sources import CheckingAgency, VirtualMedia


def print_dict_keys(d: dict, identation: int = 0):
    for k in d.keys():
        print("     " * identation + k)
        if isinstance(d[k], dict):
            print_dict_keys(d[k], identation + 1)


@dataclass
class FeedEntry:
    title: str
    link: str


class Scraper(ABC):
    news_source: Union[CheckingAgency, VirtualMedia]

    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated")

    def get_feed_entries(self) -> list[FeedEntry]:
        """Retrieve feed entries from a given source"""

        entries: list[FeedEntry] = []
        feed = parse(self.news_source.url)

        for entry in feed.entries:
            entries.append(FeedEntry(title=entry.title, link=entry.link))

        return entries

    def collect_data(self):
        """Retrieve title, description and label from each feed entry"""

        entries = self.get_feed_entries()

        if len(entries) == 0:
            print("No entries found")
            return

        entry = entries[0]
        article = Article(entry.link)
        article.download()
        article.parse()
        print(article.title)


class AosFatosScraper(Scraper):
    def __init__(self, news_source: CheckingAgency):
        self.news_source = news_source


class PiauiScraper(Scraper):
    def __init__(self, news_source: CheckingAgency):
        self.news_source = news_source


class G1Scraper(Scraper):
    def __init__(self, news_source: CheckingAgency):
        self.news_source = news_source


class EFarsasScraper(Scraper):
    def __init__(self, news_source: CheckingAgency):
        self.news_source = news_source


class BoatosScraper(Scraper):
    def __init__(self, news_source: CheckingAgency):
        self.news_source = news_source


class APublicaScraper(Scraper):
    def __init__(self, news_source: CheckingAgency):
        self.news_source = news_source


class APublicaTrucoScraper(Scraper):
    def __init__(self, news_source: CheckingAgency):
        self.news_source = news_source


class ChecamosScraper(Scraper):
    # TODO: Unable to make initial request
    def __init__(self, news_source: CheckingAgency):
        self.news_source = news_source


class G1TechScraper(Scraper):
    def __init__(self, news_source: VirtualMedia):
        self.news_source = news_source


class G1EduScraper(Scraper):
    def __init__(self, news_source: VirtualMedia):
        self.news_source = news_source


class G1EconomiaScraper(Scraper):
    def __init__(self, news_source: VirtualMedia):
        self.news_source = news_source
