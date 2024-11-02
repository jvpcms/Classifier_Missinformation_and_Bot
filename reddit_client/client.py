from typing import List, Dict, Any, Optional, TypeVar, Type
import requests
import requests.auth
import shelve

from env_config import envs
from endpoints import Endpoints, encode_url

from interfaces.subreddit_interface import SubredditInterface
from interfaces.post_interface import PostInterface

from models.subreddit_model import Subreddit
from models.user_model import User
from models.post_model import Post


T = TypeVar("T", Subreddit, User, Post)


class RedditClient:
    def __init__(self):
        self.username: str = envs.username
        self.password: str = envs.password
        self.app_id: str = envs.app_id
        self.client_secret: str = envs.client_secret

        self.store_path: str = "./shelve/local_storage"

    def authenticate(self):
        """Authencation requests, store access token"""

        client_auth = requests.auth.HTTPBasicAuth(self.app_id, self.client_secret)

        post_data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
        }

        headers = {"User-Agent": f"ChangeMeClient/0.1 by {self.username}"}

        response = requests.post(
            Endpoints.access_token, auth=client_auth, data=post_data, headers=headers
        )

        if response.status_code != 200:
            raise Exception("Authencation failed")

        with shelve.open(self.store_path) as ls:
            ls["authentication_info"] = response.json()

    @property
    def access_token(self):
        with shelve.open(self.store_path) as ls:
            if "authentication_info" not in ls:
                self.authenticate()

            return ls["authentication_info"]["access_token"]

    @property
    def default_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": f"ChangeMeClient/0.1 by {self.username}",
        }

    def subreddits(self):
        return SubredditInterface(self)

    def posts(self):
        return PostInterface(self)

    def execute(
        self,
        url: str,
        return_type: Type[T],
        query_params: Optional[Dict[str, Any]] = None,
    ) -> List[T]:
        """Execute request, return list of objects"""

        if query_params is not None:
            url = encode_url(url, query_params)

        response = requests.get(url, headers=self.default_headers)

        if response.status_code == 401:
            self.authenticate()
            response = requests.get(url, headers=self.default_headers)

        response_json = response.json()

        return [return_type.from_dict(d) for d in response_json["data"]["children"]]


if __name__ == "__main__":
    client = RedditClient()

    # subscribed_subreddits = client.subreddits().mine().subscriber().execute()
    # print(subscribed_subreddits)

    posts = client.posts().search(search_terms="python and java", limit=5).execute()
    print(posts[0].title)
    print(posts[0].selftext)
