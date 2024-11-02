import requests
from typing import TYPE_CHECKING, List, Optional, Union, Dict, Any

if TYPE_CHECKING:
    from client import RedditClient

from endpoints import Endpoints
from models.subreddit_model import Subreddit
from models.user_model import User
from models.post_model import Post


class PostInterface:
    def __init__(self, client: "RedditClient"):
        self.client = client

    def search(
        self,
        search_terms: str,
        limit: Optional[int] = None,
        search_instance: Optional[Union[User, Subreddit]] = None,
    ) -> "_SearchPosts":
        return _SearchPosts(
            self.client,
            search_terms=search_terms,
            limit=limit,
            search_instance=search_instance,
        )


class _SearchPosts:
    def __init__(
        self,
        client: "RedditClient",
        search_terms: str,
        limit: Optional[int] = None,
        search_instance: Optional[Union[User, Subreddit]] = None,
    ):
        self.client = client
        self.search_terms = search_terms
        self.limit = limit
        self.search_instance = search_instance

    def execute(self) -> List[Post]:
        if isinstance(self.search_instance, User):
            url = ""

        elif isinstance(self.search_instance, Subreddit):
            url = Endpoints.search_posts_in_subreddit.format(
                subreddit=self.search_instance.display_name
            )

        else:
            url = Endpoints.search

        params: Dict[str, Any] = {
            "q": self.search_terms,
            "type": "link",
        }

        if self.limit is not None:
            params["limit"] = self.limit

        result = self.client.execute(url, Post, query_params=params, many=True)

        if not isinstance(result, list):
            return [result]

        return result
