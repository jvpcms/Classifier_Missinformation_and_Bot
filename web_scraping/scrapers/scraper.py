from abc import ABC, abstractmethod
from typing import Union, Callable
from feedparser import FeedParserDict, parse
from newspaper import Article
from newspaper.article import requests
from newspaper.utils import BeautifulSoup

from web_scraping.models.factory import NewsSource
from web_scraping.models.labeled_news import LabeledNews
from custom_logging import logger

from utils.dictionaries import pre_processing


class Scraper(ABC):
    news_source: NewsSource

    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated")

    def get_news_feed_entries(self) -> list[FeedParserDict]:
        """Retrieve feed entries from a given source"""

        try:
            feed = parse(self.news_source.feed_url)
        except Exception as e:
            logger.error(f"Error while parsing feed: {e}")
            return []

        return feed.entries

    @abstractmethod
    def label_feed_entry(self, entry: dict) -> Union[bool, None]:
        """Label feed entry as true or false"""

    def get_article_content(self, link: str) -> dict:
        """Retrieve title, description and label from each feed entry"""

        article = Article(link)
        article.download()
        article.parse()

        with open("testing_data/article.html", "w") as f:
            f.write(article.html)

        return article.__dict__

    def collect_labeled_feed_entries(
        self, filter: Callable[[LabeledNews], bool]
    ) -> list[LabeledNews]:
        """Retrieve feed entries and label them

        * filter: Function that filters the labeled news
        """

        entries = self.get_news_feed_entries()

        feed_labeled_news: list[LabeledNews] = []

        for entry in entries:
            label = self.label_feed_entry(entry)
            labeled_news = LabeledNews.from_dict(
                {**entry, "label": label, "url_source": self.news_source.base_url}
            )

            if filter(labeled_news):
                feed_labeled_news.append(labeled_news)

        return feed_labeled_news


class AosFatosScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> Union[bool, None]:
        """Label feed entry as true or false"""
        # TODO: solve for problematic claim dict

        try:
            response = requests.get(entry["link"])
        except Exception as e:
            logger.error(f"Error / label_feed_entry / {self.__class__.__name__}: {e}")
            return None

        content = BeautifulSoup(response.content, "html.parser")
        ld_json = content.find_all("script", attrs={"type": "application/ld+json"})

        if len(ld_json) == 0:
            return None

        claim_review = ld_json[0]
        claim_dict = pre_processing(claim_review.get_text(strip=True))

        alternate_name = claim_dict.get("reviewRating", {}).get("alternateName")

        if alternate_name == "falso":
            return False

        return None


class G1Scraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> Union[bool, None]:
        """Label feed entry as true or false"""

        return False if "É #FAKE" in entry["title"] else None


class EFarsasScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def collect_labeled_feed_entries(
        self, filter: Callable[[LabeledNews], bool]
    ) -> list[LabeledNews]:
        """Retrieve feed entries and label them

        * filter: Function that filters the labeled news
        """

        true_entries = parse(self.news_source.feed_url_true_news).entries
        fake_entries = parse(self.news_source.feed_url_fake_news).entries

        feed_labeled_news: list[LabeledNews] = []

        for entry in true_entries:
            labeled_news = LabeledNews.from_dict(
                {
                    **entry,
                    "label": True,
                    "url_source": self.news_source.base_url,
                    "source_url": self.news_source.base_url,
                }
            )

            if filter(labeled_news):
                feed_labeled_news.append(labeled_news)

        for entry in fake_entries:
            labeled_news = LabeledNews.from_dict(
                {
                    **entry,
                    "label": False,
                    "url_source": self.news_source.base_url,
                    "source_url": self.news_source.base_url,
                }
            )

            if filter(labeled_news):
                feed_labeled_news.append(labeled_news)

        return feed_labeled_news

    def label_feed_entry(self, entry: dict) -> Union[bool, None]:
        """Label feed entry as true or false"""
        return None


class BoatosScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> Union[bool, None]:
        """Label feed entry as true or false"""

        response = requests.get(entry["link"])
        content = BeautifulSoup(response.content, "html.parser")

        p_tags = list(content.find_all("p"))
        p_tags_content = [p.get_text() for p in p_tags]

        try:
            p_tags_content.index("Fake news ❌")
            return False
        except ValueError:
            return None


class G1TechScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> Union[bool, None]:
        """Label feed entry as true or false"""
        return True


class G1EduScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> Union[bool, None]:
        """Label feed entry as true or false"""
        return True


class G1EconomiaScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> Union[bool, None]:
        """Label feed entry as true or false"""
        return True
