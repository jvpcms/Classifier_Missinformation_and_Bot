from abc import ABC, abstractmethod
import json
from typing import Union, Callable
from feedparser import FeedParserDict, parse
from newspaper import Article
from newspaper.article import requests
from newspaper.utils import BeautifulSoup

from web_scraping.models.factory import NewsSource
from web_scraping.models.labeled_news import LabeledNews
from custom_logging import logger

from utils.dictionaries import pre_processing


# labeled_news = LabeledNews.from_dict(
#     {**entry, "label": label, "url_source": self.news_source.base_url}
# )


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
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> LabeledNews | None:
        """Label feed entry as true or false"""
        try:
            response = requests.get(entry["link"])
            content = BeautifulSoup(response.content, "html.parser")

            description = content.find_all("meta", attrs={"name": "description"})
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

            for ld in content.find_all("script", attrs={"type": "application/ld+json"}):
                try:
                    data = json.loads(ld.get_text(strip=True))
                    claim_reviewed = claim_reviewed or data.get("claimReviewed")
                    review_body = review_body or data.get("reviewBody")

                    if "reviewRating" in data:
                        review_rating = data["reviewRating"]
                        best_rating = best_rating or review_rating.get("bestRating")
                        rating_value = rating_value or review_rating.get("ratingValue")
                        if review_rating.get("alternateName") == "falso":
                            label = False
                except json.JSONDecodeError:
                    continue

            return LabeledNews.from_dict(
                {
                    **entry,
                    "label": label,
                    "url_source": self.news_source.base_url,
                    "description": description,
                    "claim_review": claim_reviewed,
                    "review_body": review_body,
                    "best_rating": best_rating,
                    "rating_value": rating_value,
                }
            )

        except requests.RequestException as e:
            logger.error(f"Network error in label_feed_entry: {e}")
        except Exception as e:
            logger.error(f"Error in label_feed_entry: {e}")

        return None


class G1Scraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> LabeledNews | None:
        """Label feed entry as true or false"""

        response = requests.get(entry["link"])
        content = BeautifulSoup(response.content, "html.parser")

        meta_description = content.find_all("meta", attrs={"name": "description"})

        description = None
        if len(meta_description) > 0:
            description = meta_description[0].get("content")

        label = None
        if "#NÃO É BEM ASSIM" in entry["title"] or "#FAKE" in entry["title"]:
            label = False
        elif "#FATO" in entry["title"]:
            label = True

        return LabeledNews.from_dict(
            {
                **entry,
                "label": label,
                "url_source": self.news_source.base_url,
                "description": description,
            }
        )


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

        for entry in fake_entries:
            labeled_news = self.label_feed_entry(entry)

            if labeled_news is not None and filter(labeled_news):
                labeled_news.label = False
                feed_labeled_news.append(labeled_news)

        for entry in true_entries:
            labeled_news = self.label_feed_entry(entry)

            if labeled_news is not None and filter(labeled_news):
                labeled_news.label = True
                feed_labeled_news.append(labeled_news)

        return feed_labeled_news

    def label_feed_entry(self, entry: dict) -> LabeledNews | None:
        """Label feed entry as true or false"""
        try:
            response = requests.get(entry["link"])
            content = BeautifulSoup(response.content, "html.parser")

            description = content.find_all("meta", attrs={"name": "description"})
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

            for ld in content.find_all("script", attrs={"type": "application/ld+json"}):
                try:
                    data = json.loads(ld.get_text(strip=True))

                    if isinstance(data, dict):
                        data = [data]

                    for d in data:
                        claim_reviewed = claim_reviewed or d.get("claimReviewed")
                        review_body = review_body or d.get("reviewBody")

                        if "reviewRating" in d:
                            review_rating = d["reviewRating"]
                            best_rating = best_rating or review_rating.get("bestRating")
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
                    "url_source": self.news_source.base_url,
                    "description": description,
                    "claim_review": claim_reviewed,
                    "review_body": review_body,
                    "best_rating": best_rating,
                    "rating_value": rating_value,
                }
            )

        except requests.RequestException as e:
            logger.error(f"Network error in label_feed_entry: {e}")
        except Exception as e:
            logger.error(f"Error in label_feed_entry: {e}")

        return None


class BoatosScraper(Scraper):
    # TODO: language detection
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> LabeledNews | None:
        """Label feed entry as true or false"""

        response = requests.get(entry["link"])
        content = BeautifulSoup(response.content, "html.parser")

        meta_description = content.find_all("meta", attrs={"name": "description"})
        if len(meta_description) > 0:
            description = meta_description[0].get("content")
        else:
            description = None

        p_tags = content.find_all("p")
        p_tags_content = [p.get_text() for p in p_tags]

        try:
            p_tags_content.index("Fake news ❌")
            p_tags_content.index("Golpe ⚠️")
            label = False
        except ValueError:
            label = None

        return LabeledNews.from_dict(
            {
                **entry,
                "label": label,
                "url_source": self.news_source.base_url,
                "description": description,
            }
        )


class G1TechScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> LabeledNews | None:
        """Label feed entry as true or false"""

        response = requests.get(entry["link"])
        content = BeautifulSoup(response.content, "html.parser")

        meta_description = content.find_all("meta", attrs={"name": "description"})
        if len(meta_description) > 0:
            description = meta_description[0].get("content")
        else:
            description = None

        return LabeledNews.from_dict(
            {
                **entry,
                "label": True,
                "url_source": self.news_source.base_url,
                "description": description,
            }
        )


class G1EduScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> LabeledNews | None:
        """Label feed entry as true or false"""

        response = requests.get(entry["link"])
        content = BeautifulSoup(response.content, "html.parser")

        meta_description = content.find_all("meta", attrs={"name": "description"})
        if len(meta_description) > 0:
            description = meta_description[0].get("content")
        else:
            description = None

        return LabeledNews.from_dict(
            {
                **entry,
                "label": True,
                "url_source": self.news_source.base_url,
                "description": description,
            }
        )


class G1EconomiaScraper(Scraper):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source

    def label_feed_entry(self, entry: dict) -> LabeledNews | None:
        """Label feed entry as true or false"""

        response = requests.get(entry["link"])
        content = BeautifulSoup(response.content, "html.parser")

        meta_description = content.find_all("meta", attrs={"name": "description"})
        if len(meta_description) > 0:
            description = meta_description[0].get("content")
        else:
            description = None

        return LabeledNews.from_dict(
            {
                **entry,
                "label": True,
                "url_source": self.news_source.base_url,
                "description": description,
            }
        )
