from custom_logging.custom_logger import get_logger
from data_collector import data_collector_insntance

custom_logger = get_logger("main")


def main():
    """Main function to run the data collector."""

    data_collector_insntance.store_news_sources()

    collected_labaled_news = (
        data_collector_insntance.collect_labeled_news_from_all_sources(lambda _: True)
    )

    custom_logger.debug(f"#collected news: {len(collected_labaled_news)}")

    for news in collected_labaled_news:

        custom_logger.debug(f"news: {news.title}")
        data_collector_insntance.store_labeled_news(news)


if __name__ == "__main__":
    main()
