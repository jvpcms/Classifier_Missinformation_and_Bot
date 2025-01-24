from abc import ABC
from feedparser import parse
from newspaper import Article

from web_scraping.models.factory import NewsSource
from web_scraping.models.labeled_news import LabeledNews


def print_dict_keys(d: dict, identation: int = 0):
    for k in d.keys():
        print("     " * identation + k)
        if isinstance(d[k], dict):
            print_dict_keys(d[k], identation + 1)


class Scraper(ABC):
    news_source: NewsSource

    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated")

    def __get_news_feed_entries(self) -> list[dict]:
        """Retrieve feed entries from a given source"""

        feed = parse(self.news_source.feed_url)

        return feed.entries

    def __label_feed_entry(self, entry: dict) -> bool:
        """Label feed entry as true or false"""

        if self.news_source.source_type == "virtual_media":
            return True

        return False

    def __get_article_content(self, link: str) -> dict:
        """Retrieve title, description and label from each feed entry"""

        article = Article(link)
        article.download()
        article.parse()

        return article.__dict__

    def collect_labeled_feed_entries(self) -> list[LabeledNews]:
        """Retrieve feed entries and label them"""

        print(self.news_source.feed_url)
        entries = self.__get_news_feed_entries()

        if len(entries) == 0:
            return []

        feed_labeled_news: list[LabeledNews] = []

        for entry in entries:
            label = self.__label_feed_entry(entry)
            labeled_news = LabeledNews.from_dict(
                {**entry, "label": label, "url_source": self.news_source.base_url}
            )
            feed_labeled_news.append(labeled_news)

        print(f"Collected {len(feed_labeled_news)} labeled news")
        print(feed_labeled_news[0])

        return feed_labeled_news


class AosFatosScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source


class PiauiScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source


class G1Scraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source


class EFarsasScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source


class BoatosScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source


class APublicaScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source


class APublicaTrucoScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source


class ChecamosScraper(Scraper):
    # TODO: Unable to make initial request
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source


class G1TechScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source


class G1EduScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source


class G1EconomiaScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source
