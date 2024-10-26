import requests
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from client import RedditClient

from endpoints import Endpoints
from models.subreddit_model import Subreddit


class SubredditInterface:
    def __init__(self, client: "RedditClient"):
        self.client = client

    def mine(self):
        return _MineSubreddits(self.client)


class _MineSubreddits:
    def __init__(self, client: "RedditClient"):
        self.client = client

    def subscriber(self):
        return _SubscriberSubreddits(self.client)


class _SubscriberSubreddits:
    def __init__(self, client: "RedditClient"):
        self.client = client

    def execute(self) -> List[Subreddit]:
        url = Endpoints.subreddits_where_subscirbed
        headers = self.client.default_headers

        response = requests.get(url, headers=headers)
        response_json = response.json()

        return [Subreddit.from_dict(d) for d in response_json["data"]["children"]]
