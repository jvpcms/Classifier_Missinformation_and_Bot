import requests
import requests.auth
import shelve
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TypeVar, Generic

from atproto import Client

from config.envconfig import Config

from models.bluesky_post_model import BlueSkyPost
from models.bluesky_user_model import BlueSkyUser
from models.subreddit_model import Subreddit
from models.reddit_user_model import RedditUser
from models.reddit_post_model import RedditPost

from utils.endpoints import Endpoints, encode_url


PostT = TypeVar("PostT", BlueSkyPost, RedditPost)
UserT = TypeVar("UserT", BlueSkyUser, RedditUser)

ModelType = TypeVar("ModelType", Subreddit, RedditUser, RedditPost)


class SocialMediaSdk(ABC, Generic[PostT, UserT]):
    @abstractmethod
    def search_posts(self, query: str) -> List[PostT]:
        """Search posts in the social media platform"""

        raise NotImplementedError

    @abstractmethod
    def get_user_details(self, user_id: str) -> UserT:
        """Get user details in the social media platform"""

        raise NotImplementedError


class BlueSkySdk(SocialMediaSdk[BlueSkyPost, BlueSkyUser]):
    _client: Client

    def __init__(self, config: Config):
        self._client = Client()
        self._client.login(config.envs.bluesky_username, config.envs.bluesky_secret)

    def search_posts(self, query: str) -> List[BlueSkyPost]:
        response = self._client.app.bsky.feed.search_posts({"q": query})
        posts = response.posts
        return [BlueSkyPost.instantiate(post) for post in posts]

    def get_user_details(self, user_id: str) -> BlueSkyUser:
        proflie_view = self._client.app.bsky.actor.get_profile({"actor": user_id})
        return BlueSkyUser.instantiate(proflie_view)


class RedditSdk(SocialMediaSdk[RedditPost, RedditUser]):
    _username: str
    _password: str
    _app_id: str
    _client_secret: str

    _store_path: str

    def __init__(self, config: Config):
        self._username = config.envs.username
        self._password = config.envs.password
        self._app_id = config.envs.app_id
        self._client_secret = config.envs.client_secret

        self._store_path = "./social_media_api/shelve/local_storage"

    # Authentication
    @property
    def _access_token(self) -> str:
        with shelve.open(self._store_path) as ls:
            if "authentication_info" not in ls:
                self._authenticate()

            return ls["authentication_info"]["access_token"]

    @property
    def _default_headers(self) -> Dict:
        return {
            "Authorization": f"Bearer {self._access_token}",
            "User-Agent": f"ChangeMeClient/0.1 by {self._username}",
        }

    def _authenticate(self) -> None:
        """Authencation requests, store access token"""

        client_auth = requests.auth.HTTPBasicAuth(self._app_id, self._client_secret)

        post_data = {
            "grant_type": "password",
            "username": self._username,
            "password": self._password,
        }

        headers = {"User-Agent": f"ChangeMeClient/0.1 by {self._username}"}

        response = requests.post(
            Endpoints.access_token.value,
            auth=client_auth,
            data=post_data,
            headers=headers,
        )

        if response.status_code != 200:
            raise Exception("Authencation failed")

        with shelve.open(self._store_path) as ls:
            ls["authentication_info"] = response.json()

    def _api_call(
        self,
        url: str,
        query_params: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        """Execute request, return list of objects"""

        if query_params is not None:
            url = encode_url(url, query_params)

        response = requests.get(url, headers=self._default_headers)

        if response.status_code == 401:
            self._authenticate()
            response = requests.get(url, headers=self._default_headers)
        else:
            response.raise_for_status()

        return response.json()

    def search_posts(self, query: str) -> List[RedditPost]:
        url = Endpoints.search.value

        params: Dict[str, Any] = {
            "q": query,
            "type": "link",
        }

        response_json = self._api_call(url, query_params=params)
        children = response_json.get("data", {}).get("children", [])

        return [RedditPost.instatiate(child) for child in children]

    def get_user_details(self, user_id: str) -> RedditUser:
        url = Endpoints.user_about.value.format(username=user_id)
        response_json = self._api_call(url)

        return RedditUser.instantiate(response_json)
