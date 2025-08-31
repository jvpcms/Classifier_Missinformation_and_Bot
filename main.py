from custom_logging.custom_logger import get_logger
from data_collector import data_collector

custom_logger = get_logger("main")


def collect_data():
    """Main function to run the data collector."""

    data_collector.store_news_sources()

    collected_labaled_news = (
        data_collector.collect_labeled_news_from_all_sources(lambda _: True)
    )

    for news in collected_labaled_news:
        data_collector.store_labeled_news(news)

        related_posts = (
            data_collector.associate_labeled_news_with_bluesky_posts(news)
        )

        for post in related_posts:
            user = data_collector.retrieve_associated_user_from_bluesky_post(
                post
            )
            data_collector.associte_bluesky_post_with_url(post, user)

            data_collector.store_bluesky_post(post)
            data_collector.store_bluesky_user(user)


def classify_users():
    """Classify users in the database."""

    from classifier import classifiers
    from database import repos

    users = repos.bluesky_users.find()

    bot_users = []
    not_bot_users = []
    unknown_users = []

    for user in users:

        is_bot_knn = classifiers.knn_user_bot_classifier.is_bot(user)
        is_bot_dt = classifiers.decision_tree_user_bot_classifier.is_bot(user)
        is_bot_rf = classifiers.random_forest_user_bot_classifier.is_bot(user)
        is_bot_lr = classifiers.logistic_regression_user_bot_classifier.is_bot(
            user
        )
        is_bot_nn = classifiers.neural_network_user_bot_classifier.is_bot(user)

        positive_votes = sum(
            [
                is_bot_knn,
                is_bot_dt,
                is_bot_rf,
                is_bot_lr,
                is_bot_nn,
            ]
        )

        if positive_votes > 3:
            bot_users.append(user)
        elif positive_votes >= 2:
            unknown_users.append(user)
        else:
            not_bot_users.append(user)
            




if __name__ == "__main__":
    classify_users()
