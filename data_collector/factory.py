from database.factory import get_repos_collection
from social_media_api.factory import get_social_media_sdk_colleciton
from web_scraping.factory import get_scraper_collection
from custom_logging.custom_logger import get_logger

from data_collector.data_collector import DataCollector


def get_data_collector() -> DataCollector:
    """Instantiate the data collector class."""

    scraper_collection = get_scraper_collection()
    social_media_sdk_collection = get_social_media_sdk_colleciton()
    repos_collection = get_repos_collection()
    custom_logger = get_logger("data_collector")

    return DataCollector(
        scrapers_collection=scraper_collection,
        social_media_sdk_colleciton=social_media_sdk_collection,
        repos_collection=repos_collection,
        custom_logger=custom_logger,
    )
