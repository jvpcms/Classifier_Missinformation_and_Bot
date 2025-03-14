from typing import List, Optional, Union, Dict, Any

from reddit_api.services.factory import Services
from reddit_api.services.reddit_client import RedditClient

from reddit_api.utils.factory import Utils
from reddit_api.utils.endpoints import Endpoints

from reddit_api.models.subreddit_model import Subreddit
from reddit_api.models.user_model import User
from reddit_api.models.post_model import Post


class PostInterface:
    client: RedditClient
    endpoints: Endpoints

    def __init__(self, services: Services, utils: Utils):
        self.client = services.reddit_client
        self.endpoints = utils.endpoints

    def search(
        self,
        search_terms: str,
        limit: Optional[int] = None,
        search_instance: Optional[Union[User, Subreddit]] = None,
    ) -> List[Post]:
        if isinstance(search_instance, User):
            url = ""

        elif isinstance(search_instance, Subreddit):
            url = self.endpoints.search_posts_in_subreddit.format(
                subreddit=search_instance.display_name
            )

        else:
            url = self.endpoints.search

        params: Dict[str, Any] = {
            "q": search_terms,
            "type": "link",
        }

        if limit is not None:
            params["limit"] = limit

        return self.client.api_call(url, Post, query_params=params, many=True)
