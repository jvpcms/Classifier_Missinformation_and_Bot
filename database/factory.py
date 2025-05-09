from pymongo import MongoClient
from config.envconfig import Config, get_config
from database.bluesky_post_repo import BlueSkyPostRepo
from database.bluesky_user_repo import BlueSkyUserRepo
from database.labeled_news_repo import LabeledNewsRepo
from database.news_sources_repo import NewsSourcesRepo
from database.reddit_post_repo import RedditPostRepo
from database.subreddit_repo import SubredditRepo
from database.reddit_user_repo import RedditUserRepo


class ReposCollection:
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

        database = client.news_data

        self.subreddits = SubredditRepo(database)
        self.reddit_users = RedditUserRepo(database)
        self.reddit_posts = RedditPostRepo(database)
        self.bluesky_users = BlueSkyUserRepo(database)
        self.bluesky_posts = BlueSkyPostRepo(database)
        self.labeled_news = LabeledNewsRepo(database)
        self.news_sources = NewsSourcesRepo(database)


def get_repos_collection():
    config = get_config()

    return ReposCollection(config)
