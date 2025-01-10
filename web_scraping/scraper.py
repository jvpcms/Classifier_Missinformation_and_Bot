from abc import ABC
from feedparser import parse


class Scraper(ABC):
    feed_url: str

    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    def get_feed_entries(self):
        feed = parse(self.feed_url)

        for entry in feed.entries:
            print(entry.title)


class AosFatosScraper(Scraper):
    def __init__(self):
        super().__init__("https://aosfatos.org/")
