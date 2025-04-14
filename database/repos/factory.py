from pymongo import MongoClient
from database.config.factory import Config, get_config
from database.repos.bluesky_post_repo import BlueSkyPostRepo
from database.repos.bluesky_user_repo import BlueSkyUserRepo
from database.repos.labeled_news_repo import LabeledNewsRepo
from database.repos.news_sources import NewsSourcesRepo
from database.repos.reddit_post_repo import RedditPostRepo
from database.repos.subreddit_repo import SubredditRepo
from database.repos.reddit_user_repo import RedditUserRepo


class ReposFactory:
    subreddits: SubredditRepo
    reddit_users: RedditUserRepo
    reddit_posts: RedditPostRepo
    bluesky_users: BlueSkyUserRepo
    bluesky_posts: BlueSkyPostRepo
    labeled_news: LabeledNewsRepo
    news_sources: NewsSourcesRepo

    def __init__(self, config: Config):
        CONNECTION_STRING = f"mongodb://{config.envs.mongo_username}:{config.envs.mongo_password}@localhost:27017/"
        client = MongoClient(CONNECTION_STRING)

        reddit_database = client.reddit_data

        self.subreddits = SubredditRepo(reddit_database)
        self.reddit_users = RedditUserRepo(reddit_database)
        self.reddit_posts = RedditPostRepo(reddit_database)
        self.bluesky_users = BlueSkyUserRepo(reddit_database)
        self.bluesky_posts = BlueSkyPostRepo(reddit_database)
        self.labeled_news = LabeledNewsRepo(reddit_database)
        self.news_sources = NewsSourcesRepo(reddit_database)


def get_repos():
    config = get_config()

    return ReposFactory(config)
