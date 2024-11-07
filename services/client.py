from typing import List, Dict, Any, Optional, TypeVar, Type, Union, overload
import requests
import requests.auth
import shelve

from utils.endpoints import Endpoints
from utils.parser import Parser
from utils.factory import Utils

from models.subreddit_model import Subreddit
from models.user_model import User
from models.post_model import Post


ModelType = TypeVar("ModelType", Subreddit, User, Post)


class RedditClient:
    endpoints: Endpoints
    parser: Parser

    username: str
    password: str
    app_id: str
    client_secret: str

    store_path: str

    def __init__(self, utils: Utils):
        self.endpoints = utils.endpoints
        self.parser = utils.parser

        self.username = utils.envs.username
        self.password = utils.envs.password
        self.app_id = utils.envs.app_id
        self.client_secret = utils.envs.client_secret

        self.store_path = "./shelve/local_storage"

    # Authentication
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
            self.endpoints.access_token,
            auth=client_auth,
            data=post_data,
            headers=headers,
        )

        if response.status_code != 200:
            raise Exception("Authencation failed")

        with shelve.open(self.store_path) as ls:
            ls["authentication_info"] = response.json()

    # Execute API requests
    @overload
    def api_call(
        self,
        url: str,
        return_type: Type[ModelType],
        *,
        query_params: Optional[Dict[str, Any]] = None,
    ) -> ModelType: ...

    @overload
    def api_call(
        self,
        url: str,
        return_type: Type[ModelType],
        *,
        many: bool,
        query_params: Optional[Dict[str, Any]] = None,
    ) -> List[ModelType]: ...

    def api_call(
        self,
        url: str,
        return_type: Type[ModelType],
        *,
        many: bool = False,
        query_params: Optional[Dict[str, Any]] = None,
    ) -> Union[ModelType, List[ModelType]]:
        """Execute request, return list of objects"""

        if query_params is not None:
            url = self.endpoints.encode_url(url, query_params)

        response = requests.get(url, headers=self.default_headers)

        if response.status_code == 401:
            self.authenticate()
            response = requests.get(url, headers=self.default_headers)

        response_json = response.json()

        return self.parser.parse(response_json, return_type, many=many)
