from utils.factory import get_utils

from client import RedditClient


class Services:
    reddit_client: RedditClient

    def __init__(self, reddit_client: RedditClient):
        self.reddit_client = reddit_client


def get_services():
    utils = get_utils()
    reddit_client = RedditClient(utils)

    return Services(reddit_client)
