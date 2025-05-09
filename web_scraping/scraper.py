from abc import ABC, abstractmethod
import json
from typing import Callable
from feedparser import FeedParserDict, parse
from newspaper import Article
from newspaper.article import requests
from newspaper.utils import BeautifulSoup

from custom_logging.custom_logger import CustomLogger
from models.news_sources import NewsSource
from models.labeled_news import LabeledNews


class Scraper(ABC):
    news_source: NewsSource
    custom_logger: CustomLogger

    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated")

    def get_news_feed_entries(self) -> list[FeedParserDict]:
        """Retrieve feed entries from a given source"""

        try:
            feed = parse(self.news_source.feed_url)
        except Exception as e:
            self.custom_logger.error(f"Error while parsing feed: {e}")
            return []

        return feed.entries

    @abstractmethod
    def label_feed_entry(self, entry: dict) -> LabeledNews | None:
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
            labeled_news = self.label_feed_entry(entry)

            if labeled_news is not None and filter(labeled_news):
                feed_labeled_news.append(labeled_news)

        return feed_labeled_news


class AosFatosScraper(Scraper):
    def __init__(self, news_source: NewsSource, custom_logger: CustomLogger):
        self.news_source = news_source
        self.custom_logger = custom_logger

    def label_feed_entry(self, entry: dict) -> LabeledNews | None:
        """Label feed entry as true or false"""
        try:
            response = requests.get(entry["link"])
            content = BeautifulSoup(response.content, "html.parser")

            description = content.find_all(
                "meta", attrs={"name": "description"}
            )
            if len(description) > 0:
                description = description[0].get("content")
            else:
                description = None

            claim_reviewed, review_body, best_rating, rating_value, label = (
                None,
                None,
                None,
                None,
                None,
            )

            for ld in content.find_all(
                "script", attrs={"type": "application/ld+json"}
            ):
                try:
                    data = json.loads(ld.get_text(strip=True))
                    claim_reviewed = claim_reviewed or data.get("claimReviewed")
                    review_body = review_body or data.get("reviewBody")

                    if "reviewRating" in data:
                        review_rating = data["reviewRating"]
                        best_rating = best_rating or review_rating.get(
                            "bestRating"
                        )
                        rating_value = rating_value or review_rating.get(
                            "ratingValue"
                        )
                        if review_rating.get("alternateName") == "falso":
                            label = False
                except json.JSONDecodeError:
                    continue

            return LabeledNews.from_dict(
                {
                    **entry,
                    "label": label,
                    "source_url": self.news_source.base_url,
                    "description": description,
                    "claim_review": claim_reviewed,
                    "review_body": review_body,
                    "best_rating": best_rating,
                    "rating_value": rating_value,
                }
            )

        except requests.RequestException as e:
            self.custom_logger.error(f"Network error in label_feed_entry: {e}")
        except Exception as e:
            self.custom_logger.error(f"Error in label_feed_entry: {e}")

        return None


class G1Scraper(Scraper):
    def __init__(self, news_source: NewsSource, custom_logger: CustomLogger):
        self.news_source = news_source
        self.custom_logger = custom_logger

    def label_feed_entry(self, entry: dict) -> LabeledNews | None:
        """Label feed entry as true or false"""

        response = requests.get(entry["link"])
        content = BeautifulSoup(response.content, "html.parser")

        meta_description = content.find_all(
            "meta", attrs={"name": "description"}
        )

        description = None
        if len(meta_description) > 0:
            description = meta_description[0].get("content")

        label = None

        if any(
            keyword in entry["title"]
            for keyword in ["#NÃO É BEM ASSIM", "#FAKE", "#É FAKE"]
        ):
            label = False
        elif "#FATO" in entry["title"]:
            label = True

        return LabeledNews.from_dict(
            {
                **entry,
                "label": label,
                "source_url": self.news_source.base_url,
                "description": description,
            }
        )


class EFarsasScraper(Scraper):
    def __init__(self, news_source: NewsSource, custom_logger: CustomLogger):
        self.news_source = news_source
        self.custom_logger = custom_logger

    def collect_labeled_feed_entries(
        self, filter: Callable[[LabeledNews], bool]
    ) -> list[LabeledNews]:
        """Retrieve feed entries and label them

        * filter: Function that filters the labeled news
        """

        true_entries = parse(self.news_source.feed_url_true_news).entries
        fake_entries = parse(self.news_source.feed_url_fake_news).entries

        feed_labeled_news: list[LabeledNews] = []

        for entry in fake_entries:
            labeled_news = self.retrieve_extra_data(entry)

            if labeled_news is not None and filter(labeled_news):
                labeled_news.label = False
                feed_labeled_news.append(labeled_news)

        for entry in true_entries:
            labeled_news = self.retrieve_extra_data(entry)

            if labeled_news is not None and filter(labeled_news):
                labeled_news.label = True
                feed_labeled_news.append(labeled_news)

        return feed_labeled_news

    def retrieve_extra_data(self, entry: dict) -> LabeledNews | None:
        """Add claim review, review body, best rating and rating value to the entry"""
        try:
            response = requests.get(entry["link"])
            content = BeautifulSoup(response.content, "html.parser")

            description = content.find_all(
                "meta", attrs={"name": "description"}
            )
            if len(description) > 0:
                description = description[0].get("content")
            else:
                description = None

            claim_reviewed, review_body, best_rating, rating_value, label = (
                None,
                None,
                None,
                None,
                None,
            )

            for ld in content.find_all(
                "script", attrs={"type": "application/ld+json"}
            ):
                try:
                    data = json.loads(ld.get_text(strip=True))

                    if isinstance(data, dict):
                        data = [data]

                    for d in data:
                        claim_reviewed = claim_reviewed or d.get(
                            "claimReviewed"
                        )
                        review_body = review_body or d.get("reviewBody")

                        if "reviewRating" in d:
                            review_rating = d["reviewRating"]
                            best_rating = best_rating or review_rating.get(
                                "bestRating"
                            )
                            rating_value = rating_value or review_rating.get(
                                "ratingValue"
                            )
                            if review_rating.get("alternateName") == "falso":
                                label = False
                except json.JSONDecodeError:
                    continue

            return LabeledNews.from_dict(
                {
                    **entry,
                    "label": label,
                    "source_url": self.news_source.base_url,
                    "description": description,
                    "claim_review": claim_reviewed,
                    "review_body": review_body,
                    "best_rating": best_rating,
                    "rating_value": rating_value,
                }
            )

        except requests.RequestException as e:
            self.custom_logger.error(f"Network error in label_feed_entry: {e}")
        except Exception as e:
            self.custom_logger.error(f"Error in label_feed_entry: {e}")

        return None

    def label_feed_entry(self, entry: dict) -> LabeledNews | None:
        return None


class BoatosScraper(Scraper):
    def __init__(self, news_source: NewsSource, custom_logger: CustomLogger):
        self.news_source = news_source
        self.custom_logger = custom_logger

    def label_feed_entry(self, entry: dict) -> LabeledNews | None:
        """Label feed entry as true or false"""

        if str(entry["link"]).startswith(
            "https://www.boatos.org/english/"
        ) or str(entry["link"]).startswith("https://www.boatos.org/espanol/"):
            return None

        response = requests.get(entry["link"])
        content = BeautifulSoup(response.content, "html.parser")

        meta_description = content.find_all(
            "meta", attrs={"name": "description"}
        )
        if len(meta_description) > 0:
            description = meta_description[0].get("content")
        else:
            description = None

        p_tags = content.find_all("p")

        label = None

        for tag in p_tags:
            if tag.get_text() in ["Fake news ❌", "Golpe ⚠️"]:
                label = False
                break

        return LabeledNews.from_dict(
            {
                **entry,
                "label": label,
                "source_url": self.news_source.base_url,
                "description": description,
            }
        )


class G1TechScraper(Scraper):
    def __init__(self, news_source: NewsSource, custom_logger: CustomLogger):
        self.news_source = news_source
        self.custom_logger = custom_logger

    def label_feed_entry(self, entry: dict) -> LabeledNews | None:
        """Label feed entry as true or false"""

        response = requests.get(entry["link"])
        content = BeautifulSoup(response.content, "html.parser")

        meta_description = content.find_all(
            "meta", attrs={"name": "description"}
        )
        if len(meta_description) > 0:
            description = meta_description[0].get("content")
        else:
            description = None

        return LabeledNews.from_dict(
            {
                **entry,
                "label": True,
                "source_url": self.news_source.base_url,
                "description": description,
            }
        )


class G1EduScraper(Scraper):
    def __init__(self, news_source: NewsSource, custom_logger: CustomLogger):
        self.news_source = news_source
        self.custom_logger = custom_logger

    def label_feed_entry(self, entry: dict) -> LabeledNews | None:
        """Label feed entry as true or false"""

        response = requests.get(entry["link"])
        content = BeautifulSoup(response.content, "html.parser")

        meta_description = content.find_all(
            "meta", attrs={"name": "description"}
        )
        if len(meta_description) > 0:
            description = meta_description[0].get("content")
        else:
            description = None

        return LabeledNews.from_dict(
            {
                **entry,
                "label": True,
                "source_url": self.news_source.base_url,
                "description": description,
            }
        )


class G1EconomiaScraper(Scraper):
    def __init__(self, news_source: NewsSource, custom_logger: CustomLogger):
        self.news_source = news_source
        self.custom_logger = custom_logger

    def label_feed_entry(self, entry: dict) -> LabeledNews | None:
        """Label feed entry as true or false"""

        response = requests.get(entry["link"])
        content = BeautifulSoup(response.content, "html.parser")

        meta_description = content.find_all(
            "meta", attrs={"name": "description"}
        )
        if len(meta_description) > 0:
            description = meta_description[0].get("content")
        else:
            description = None

        return LabeledNews.from_dict(
            {
                **entry,
                "label": True,
                "source_url": self.news_source.base_url,
                "description": description,
            }
        )
