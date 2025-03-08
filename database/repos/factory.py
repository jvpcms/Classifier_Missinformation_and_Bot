from pymongo import MongoClient
from database.config.factory import Config, get_config
from database.repos.labeled_news_repo import LabeledNewsRepo
from database.repos.news_sources import NewsSourcesRepo
from database.repos.post_repo import PostRepo
from database.repos.subreddit_repo import SubredditRepo
from database.repos.user_repo import UserRepo


class ReposFactory:
    subreddits: SubredditRepo
    users: UserRepo
    posts: PostRepo
    labeled_news: LabeledNewsRepo
    news_sources: NewsSourcesRepo

    def __init__(self, config: Config):
        CONNECTION_STRING = f"mongodb://{config.envs.mongo_username}:{config.envs.mongo_password}@localhost:27017/"
        client = MongoClient(CONNECTION_STRING)

        reddit_database = client.reddit_data

        self.subreddits = SubredditRepo(reddit_database)
        self.users = UserRepo(reddit_database)
        self.posts = PostRepo(reddit_database)
        self.labeled_news = LabeledNewsRepo(reddit_database)
        self.news_sources = NewsSourcesRepo(reddit_database)


def get_repos():
    config = get_config()

    return ReposFactory(config)
