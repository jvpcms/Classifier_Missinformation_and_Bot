from custom_logging.custom_logger import get_logger
from data_collector import data_collector_insntance

custom_logger = get_logger("main")


def main():
    """Main function to run the data collector."""

    data_collector_insntance.store_news_sources()

    collected_labaled_news = (
        data_collector_insntance.collect_labeled_news_from_all_sources(lambda _: True)
    )

    for news in collected_labaled_news:
        data_collector_insntance.store_labeled_news(news)

        related_posts = (
            data_collector_insntance.associate_labeled_news_with_bluesky_posts(news)
        )

        for post in related_posts:
            user = data_collector_insntance.retrieve_associated_user_from_bluesky_post(
                post
            )
            data_collector_insntance.associte_bluesky_post_with_url(post, user)

            data_collector_insntance.store_bluesky_post(post)
            data_collector_insntance.store_bluesky_user(user)


if __name__ == "__main__":
    main()
