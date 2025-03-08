from abc import ABC, abstractmethod
from time import sleep
from typing import Union
from feedparser import parse
from newspaper import Article
from newspaper.article import requests
from newspaper.utils import BeautifulSoup

from web_scraping.models.factory import NewsSource
from web_scraping.models.labeled_news import LabeledNews
from custom_logging import logger
import re
import json
from xml.sax import saxutils
import urllib.parse


def print_dict_keys(d: dict, identation: int = 0):
    for k in d.keys():
        print("     " * identation + k)
        if isinstance(d[k], dict):
            print_dict_keys(d[k], identation + 1)


def extract_specific_key(json_string: str, key: str) -> str:
    """Search for a specific key in a json string, return the portion of the string containing the key and its value"""

    match_string = f'"{key}":'

    start = json_string.find(match_string)
    if start == -1:
        return ""

    start += len(match_string)
    end = start

    while json_string[end] not in ["}"]:
        end += 1

    return json_string[start : end + 1]


def pre_processing(str) -> dict:
    """Pre-process a string to extract a json object"""

    new_string = saxutils.unescape(str.replace("&quot;", ""))
    new_string = re.sub(
        "[^A-Za-z0-9 \\!\\@\\#\\$\\%\\&\\*\\:\\,\\.\\;\\:\\-\\_\\\"'\\]\\[\\}\\{\\+\\á\\à\\é\\è\\í\\ì\\ó\\ò\\ú\\ù\\ã\\õ\\â\\ê\\ô\\ç\\|]+",
        "",
        new_string,
    )

    try:
        new_dict = json.loads(new_string)
    except Exception:
        new_string = extract_specific_key(new_string, "reviewRating")

        try:
            new_dict = json.loads(new_string)
            return {"reviewRating": new_dict}
        except Exception as e:
            logger.error(f"Error while parsing json / pre_processing: {e}")
            return {}

    if (
        "@graph" in new_dict
        and isinstance(new_dict["@graph"], list)
        and len(new_dict["@graph"]) > 0
    ):
        new_dict = new_dict["@graph"][0]

    return new_dict


class Scraper(ABC):
    news_source: NewsSource

    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated")

    def get_news_feed_entries(self) -> list[dict]:
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

    def collect_labeled_feed_entries(self) -> list[LabeledNews]:
        """Retrieve feed entries and label them"""

        entries = self.get_news_feed_entries()

        feed_labeled_news: list[LabeledNews] = []

        for entry in entries:
            label = self.label_feed_entry(entry)
            labeled_news = LabeledNews.from_dict(
                {**entry, "label": label, "author": self.news_source.base_url}
            )
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


class PiauiScraper(Scraper):
    # TODO: Unable to make article request
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> Union[bool, None]:
        """Label feed entry as true or false"""

        response = requests.get(entry["link"])
        print(response.text)

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

    def collect_labeled_feed_entries(self) -> list[LabeledNews]:
        """Retrieve feed entries and label them"""

        true_entries = parse(self.news_source.feed_url_true_news).entries
        fake_entries = parse(self.news_source.feed_url_fake_news).entries

        feed_labeled_news: list[LabeledNews] = []

        for entry in true_entries:
            labeled_news = LabeledNews.from_dict(
                {**entry, "label": True, "url_source": self.news_source.base_url}
            )
            feed_labeled_news.append(labeled_news)

        for entry in fake_entries:
            labeled_news = LabeledNews.from_dict(
                {**entry, "label": False, "url_source": self.news_source.base_url}
            )
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


class APublicaScraper(Scraper):
    # TODO: Unable to make article request
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> Union[bool, None]:
        """Label feed entry as true or false"""

        print(entry["link"])
        return None


class APublicaTrucoScraper(Scraper):
    # TODO: Unable to make article request
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> Union[bool, None]:
        """Label feed entry as true or false"""

        return None


class ChecamosScraper(Scraper):
    # TODO: Unable to make feed request
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> Union[bool, None]:
        """Label feed entry as true or false"""

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
