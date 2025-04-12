from pymongo import MongoClient
from database.config.factory import Config, get_config
from database.repos.labeled_news_repo import LabeledNewsRepo
from database.repos.news_sources import NewsSourcesRepo
from database.repos.reddit_post_repo import RedditPostRepo
from database.repos.subreddit_repo import SubredditRepo
from database.repos.reddit_user_repo import RedditUserRepo


class ReposFactory:
    subreddits: SubredditRepo
    users: RedditUserRepo
    posts: RedditPostRepo
    labeled_news: LabeledNewsRepo
    news_sources: NewsSourcesRepo

    def __init__(self, config: Config):
        CONNECTION_STRING = f"mongodb://{config.envs.mongo_username}:{config.envs.mongo_password}@localhost:27017/"
        client = MongoClient(CONNECTION_STRING)

        reddit_database = client.reddit_data

        self.subreddits = SubredditRepo(reddit_database)
        self.users = RedditUserRepo(reddit_database)
        self.posts = RedditPostRepo(reddit_database)
        self.labeled_news = LabeledNewsRepo(reddit_database)
        self.news_sources = NewsSourcesRepo(reddit_database)


def get_repos():
    config = get_config()

    return ReposFactory(config)
