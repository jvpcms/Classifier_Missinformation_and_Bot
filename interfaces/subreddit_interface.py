from typing import List

from services.factory import Services
from utils.factory import Utils

from models.subreddit_model import Subreddit


class SubredditInterface:
    def __init__(self, services: Services, utils: Utils):
        self.client = services.reddit_client
        self.endpoints = utils.endpoints

    def subscriber_subreddits(self) -> List[Subreddit]:
        url = self.endpoints.subreddits_where_subscirbed
        return self.client.execute(url, Subreddit, many=True)

    def about(self, display_name: str) -> Subreddit:
        url = self.endpoints.subreddits_about.format(subreddit=display_name)
        return self.client.execute(url, Subreddit)
