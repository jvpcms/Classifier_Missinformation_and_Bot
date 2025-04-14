import urllib.parse
from typing import Dict
from enum import Enum

URL = "https://www.reddit.com"
OAUTH_URL = "https://oauth.reddit.com"


class Endpoints(Enum):
    access_token = URL + "/api/v1/access_token"
    user_about = OAUTH_URL + "/user/{username}/about"
    search = OAUTH_URL + "/search"


def encode_url(url: str, query_params: Dict[str, str]) -> str:
    return url + "?" + urllib.parse.urlencode(query_params)
