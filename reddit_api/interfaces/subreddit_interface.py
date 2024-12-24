from typing import List

from reddit_api.services.factory import Services
from reddit_api.services.reddit_client import RedditClient

from reddit_api.utils.factory import Utils
from reddit_api.utils.endpoints import Endpoints

from reddit_api.models.subreddit_model import Subreddit


class SubredditInterface:
    client: RedditClient
    endpoints: Endpoints

    def __init__(self, services: Services, utils: Utils):
        self.client = services.reddit_client
        self.endpoints = utils.endpoints

    def subscriber_subreddits(self) -> List[Subreddit]:
        url = self.endpoints.subreddits_where_subscirbed
        return self.client.api_call(url, Subreddit, many=True)

    def about(self, display_name: str) -> Subreddit:
        url = self.endpoints.subreddits_about.format(subreddit=display_name)
        return self.client.api_call(url, Subreddit)
