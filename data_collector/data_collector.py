from pymongo import errors as pymongo_errors

from typing import List, Callable
from custom_logging.custom_logger import CustomLogger
from database.factory import ReposCollection

from models.labeled_news import LabeledNews
from web_scraping.factory import ScraperCollection

from social_media_api.factory import SocialMediaSdkCollection

from models.bluesky_post_model import BlueSkyPost
from models.bluesky_user_model import BlueSkyUser


class DataCollector:
    """
    1. Store news sources
    2. Scrape labeled news
    3. Store scraped news in the database
    4. Associate labeled news with social media posts
    5. Store social media posts in the database
    6. Retrieve social media user information
    7. Store social media user information in the database
    """

    scrapers_collection: ScraperCollection
    social_media_sdk_colleciton: SocialMediaSdkCollection
    repos_collection: ReposCollection
    custom_logger: CustomLogger

    def __init__(
        self,
        scrapers_collection: ScraperCollection,
        social_media_sdk_colleciton: SocialMediaSdkCollection,
        repos_collection: ReposCollection,
        custom_logger: CustomLogger,
    ):
        self.scrapers_collection = scrapers_collection
        self.social_media_sdk_colleciton = social_media_sdk_colleciton
        self.repos_collection = repos_collection
        self.custom_logger = custom_logger

    def store_news_sources(self):
        """Store news sources in the database"""

        for scraper in self.scrapers_collection.get_scrapers():
            try:
                self.repos_collection.news_sources.insert(scraper.news_source)
            except pymongo_errors.DuplicateKeyError:
                self.custom_logger.debug(
                    f"Duplicate key error for {scraper.news_source.base_url}"
                )

            except Exception as e:
                self.custom_logger.error(
                    f"Error storing news source {scraper.news_source.base_url}: {e}"
                )

    def collect_labeled_news_from_all_sources(
        self, filter_function: Callable[[LabeledNews], bool]
    ) -> List[LabeledNews]:
        """Collect labeled news from scrapers and store in the database"""

        collected_labeled_news: List[LabeledNews] = []

        for scraper in self.scrapers_collection.get_scrapers():

            self.custom_logger.debug(f"Scraping {scraper.__class__}")
            try:
                labeled_news = scraper.collect_labeled_feed_entries(filter_function)
                labeled_news = list(filter(lambda x: x.label is not None, labeled_news))

                collected_labeled_news = collected_labeled_news + labeled_news

            except Exception as e:
                self.custom_logger.error(f"Error scraping {scraper.__class__}: {e}")

        return collected_labeled_news

    def store_labeled_news(self, labeled_news: LabeledNews) -> None:
        """Store labeled news in the database"""

        try:
            self.repos_collection.labeled_news.insert(labeled_news)

        except pymongo_errors.DuplicateKeyError:
            self.custom_logger.debug(
                f"Duplicate key error for news {labeled_news.link}"
            )

        except Exception as e:
            self.custom_logger.error(f"Error storing news {labeled_news.link}: {e}")

    def associate_labeled_news_with_bluesky_posts(
        self, labeled_news: LabeledNews
    ) -> List[BlueSkyPost]:
        """Associate labeled news with social media posts"""

        query = labeled_news.get_search_query()

        if query is None or len(query) == 0:
            return []

        related_posts = self.social_media_sdk_colleciton.bluesky_sdk.search_posts(
            query
        )

        for post in related_posts:
            post.associate_with_labeled_news(labeled_news)

        return related_posts

    def retrieve_associated_user_from_bluesky_post(self, post: BlueSkyPost) -> BlueSkyUser:
        return self.social_media_sdk_colleciton.bluesky_sdk.get_user_details(post.user_did)

    def associte_bluesky_post_with_url(self, post: BlueSkyPost, user: BlueSkyUser):
        post.associate_with_link(user)

    def store_bluesky_post(self, bluesky_post: BlueSkyPost) -> None:
        """Store bluesky post in database"""

        try:
            self.repos_collection.bluesky_posts.insert(bluesky_post)
        except pymongo_errors.DuplicateKeyError:
            self.custom_logger.debug(f"Duplicate key error for {bluesky_post.uri}")

        except Exception as e:
            self.custom_logger.error(
                f"Error storing bluesky post {bluesky_post.uri}: {e}"
            )

    def collect_bluesky_acconunt_info(self, bluesky_post: BlueSkyPost) -> BlueSkyUser:
        """Retrieve poster account from bluesky post"""

        user_id = bluesky_post.user_did

        return self.social_media_sdk_colleciton.bluesky_sdk.get_user_details(user_id)

    def store_bluesky_user(self, bluesky_user: BlueSkyUser) -> None:
        """Store bluesky post in database"""

        try:
            self.repos_collection.bluesky_users.insert(bluesky_user)
        except pymongo_errors.DuplicateKeyError:
            self.custom_logger.debug(f"Duplicate key error for {bluesky_user.did}")

        except Exception as e:
            self.custom_logger.error(
                f"Error storing bluesky post {bluesky_user.did}: {e}"
            )
