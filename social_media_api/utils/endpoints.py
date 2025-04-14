import urllib.parse
from typing import Dict


class Endpoints:
    URL = "https://www.reddit.com"
    OAUTH_URL = "https://oauth.reddit.com"

    # AUTHENTICATION
    access_token = URL + "/api/v1/access_token"

    # USERS
    user_about = OAUTH_URL + "/user/{username}/about"

    # SEARCH
    search = OAUTH_URL + "/search"

    @staticmethod
    def encode_url(url: str, query_params: Dict[str, str]) -> str:
        return url + "?" + urllib.parse.urlencode(query_params)
