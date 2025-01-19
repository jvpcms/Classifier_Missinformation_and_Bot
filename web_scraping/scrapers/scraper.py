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
    # TODO: Unable to open articles
    def __init__(self, news_source: CheckingAgency):
        self.news_source = news_source


class G1Scraper(Scraper):
    def __init__(self, news_source: CheckingAgency):
        self.news_source = news_source

    # Override
    def get_feed_entries(self) -> list[FeedEntry]:
        entries: list[FeedEntry] = []
        feed_content = requests.get(self.news_source.url).content
        soup = BeautifulSoup(feed_content, "html.parser")

        # Feed entries are in the h2 tags
        # TODO: This is not reliable
        h2_tags = soup.select("h2")

        for entry in h2_tags:
            link_tag = entry.select_one("a")
            title_tag = entry.select_one("p")

            if title_tag is None or link_tag is None:
                continue

            title = title_tag.get_text()
            link = link_tag.get("href")

            if link is None:
                continue

            if isinstance(link, list):
                link = link[0]

            entries.append(FeedEntry(title=title, link=link))

        return entries


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
