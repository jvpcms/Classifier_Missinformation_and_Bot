from typing import List, Dict, Any, Optional, TypeVar, Type, Union, overload
import requests
import requests.auth
import shelve

from env_config import envs
from endpoints import Endpoints, encode_url

from interfaces.subreddit_interface import SubredditInterface
from interfaces.post_interface import PostInterface
from interfaces.user_interface import UserInterface

from models.subreddit_model import Subreddit
from models.user_model import User
from models.post_model import Post

from utils.parser import parse


ModelType = TypeVar("ModelType", Subreddit, User, Post)


class RedditClient:
    def __init__(self):
        self.username: str = envs.username
        self.password: str = envs.password
        self.app_id: str = envs.app_id
        self.client_secret: str = envs.client_secret

        self.store_path: str = "./shelve/local_storage"

    # Authentication
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

    # Interfaces
    def subreddits(self):
        return SubredditInterface(self)

    def posts(self):
        return PostInterface(self)

    def users(self):
        return UserInterface(self)

    # Execute API requests
    @overload
    def execute(
        self,
        url: str,
        return_type: Type[ModelType],
        *,
        query_params: Optional[Dict[str, Any]] = None,
    ) -> ModelType: ...

    @overload
    def execute(
        self,
        url: str,
        return_type: Type[ModelType],
        *,
        many: bool,
        query_params: Optional[Dict[str, Any]] = None,
    ) -> List[ModelType]: ...

    def execute(
        self,
        url: str,
        return_type: Type[ModelType],
        *,
        many: bool = False,
        query_params: Optional[Dict[str, Any]] = None,
    ) -> Union[ModelType, List[ModelType]]:
        """Execute request, return list of objects"""

        if query_params is not None:
            url = encode_url(url, query_params)

        response = requests.get(url, headers=self.default_headers)

        if response.status_code == 401:
            self.authenticate()
            response = requests.get(url, headers=self.default_headers)

        response_json = response.json()

        return parse(response_json, return_type, many=many)


if __name__ == "__main__":
    client = RedditClient()

    usr = client.users().about("Garfield_Car").execute()
    print(usr)
