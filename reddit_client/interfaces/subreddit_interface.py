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

    def about(self, display_name: str) -> "_AboutSubreddits":
        return _AboutSubreddits(self.client, display_name)


# Mine subreddits
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
        result = self.client.execute(url, Subreddit, many=True)

        if not isinstance(result, list):
            return [result]

        return result


# Search subreddits
class _SearchSubreddits:
    def __init__(self, client: "RedditClient"):
        self.client = client


# About subreddits
class _AboutSubreddits:
    def __init__(self, client: "RedditClient", display_name: str):
        self.client = client
        self.display_name = display_name

    def execute(self) -> Subreddit:
        url = Endpoints.subreddits_about.format(subreddit=self.display_name)

        resut = self.client.execute(url, Subreddit)

        if isinstance(resut, list):
            return resut[0]

        return resut
