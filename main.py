from custom_logging.custom_logger import get_logger
from data_collector import data_collector_insntance
from datetime import datetime, timedelta

from database.factory import get_repos_collection
from models.labeled_news import LabeledNews

custom_logger = get_logger("main")

DATE_LIMIT = datetime.now() - timedelta(days=7)

repo_collection = get_repos_collection()


def labeled_news_filer_function(labeled_news: LabeledNews) -> bool:
    """Filter labeled news by date"""

    # date_limit = datetime.now() - timedelta(days=7)
    #
    # return (labeled_news.date_published is not None) and (
    #     labeled_news.date_published > date_limit
    # )
    return True


repo_collection = get_repos_collection()


def test():
    """Test function to check the functionality of the data collector."""

    false_news = repo_collection.labeled_news.find({"label": False})
    print(f"Total false news: {len(false_news)}")
    true_news = repo_collection.labeled_news.find({"label": True})
    print(f"Total true news: {len(true_news)}")


def main():
    """Main function to run the data collector."""

    labeled_news = repo_collection.labeled_news.find()
    print(f"Total labeled news: {len(labeled_news)}")
    # data_collector_insntance.store_news_sources()
    #
    # collected_labaled_news = (
    #     data_collector_insntance.collect_labeled_news_from_all_sources(
    #         labeled_news_filer_function
    #     )
    # )
    #
    # custom_logger.debug(f"#collected news: {len(collected_labaled_news)}")
    #
    # for news in collected_labaled_news:
    #
    #     custom_logger.debug(f"news: {news.title}")
    #     data_collector_insntance.store_labeled_news(news)


if __name__ == "__main__":
    # main()
    test()
