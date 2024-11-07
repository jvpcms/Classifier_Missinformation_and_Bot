from utils.factory import Utils, get_utils

from client import RedditClient


class Services:
    reddit_client: RedditClient

    def __init__(self, utils: Utils):
        self.reddit_client = RedditClient(utils)


def get_services():
    utils = get_utils()
    return Services(utils)
