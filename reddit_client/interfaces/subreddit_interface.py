from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from client import RedditClient

from endpoints import Endpoints
from models.subreddit_model import Subreddit


class SubredditInterface:
    def __init__(self, client: "RedditClient"):
        self.client = client

    def mine(self) -> "_MineSubreddits":
        return _MineSubreddits(self.client)

    def search(self) -> "_SearchSubreddits":
        return _SearchSubreddits(self.client)


class _MineSubreddits:
    def __init__(self, client: "RedditClient"):
        self.client = client

    def subscriber(self) -> "_SubscriberSubreddits":
        return _SubscriberSubreddits(self.client)


class _SubscriberSubreddits:
    def __init__(self, client: "RedditClient"):
        self.client = client

    def execute(self) -> List[Subreddit]:
        url = Endpoints.subreddits_where_subscirbed
        return self.client.execute(url, Subreddit)


class _SearchSubreddits:
    def __init__(self, client: "RedditClient"):
        self.client = client
