from abc import ABC
from feedparser import parse
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


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
    feed_url: str

    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    def get_feed_entries(self) -> list[FeedEntry]:
        entries: list[FeedEntry] = []
        feed = parse(self.feed_url)

        for entry in feed.entries:
            entries.append(FeedEntry(title=entry.title, link=entry.link))

        return entries


class AosFatosScraper(Scraper):
    def __init__(self):
        super().__init__(feed_url="https://aosfatos.org/noticias/feed/")


class PiauiScraper(Scraper):
    def __init__(self):
        super().__init__(feed_url="https://piaui.folha.uol.com.br/lupa/feed/")


class G1Scraper(Scraper):
    def __init__(self):
        super().__init__(
            feed_url="https://g1.globo.com/fato-ou-fake/",
        )

    # Override
    def get_feed_entries(self) -> list[FeedEntry]:
        entries: list[FeedEntry] = []
        feed_content = requests.get(self.feed_url).content
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


class EFersasScraper(Scraper):
    def __init__(self):
        super().__init__(
            feed_url="https://www.e-farsas.com/feed",
        )


class BoatosScraper(Scraper):
    def __init__(self):
        super().__init__(
            feed_url="https://www.boatos.org/feed",
        )


class APublicaScraper(Scraper):
    def __init__(self):
        super().__init__(
            feed_url="https://apublica.org/feed/",
        )


class APublicaTrucoScraper(Scraper):
    def __init__(self):
        super().__init__(
            feed_url="https://apublica.org/tag/truco/feed/",
        )


class ChecamosScraper(Scraper):
    # TODO: Unable to make request
    def __init__(self):
        super().__init__(feed_url="https://checamos.afp.com")
