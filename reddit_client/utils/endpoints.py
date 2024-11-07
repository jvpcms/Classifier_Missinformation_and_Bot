import urllib.parse
from typing import Dict

URL = "https://www.reddit.com"
OAUTH_URL = "https://oauth.reddit.com"


class Endpoints:
    # AUTHENTICATION
    access_token = URL + "/api/v1/access_token"

    # ME
    me = OAUTH_URL + "/api/v1/me"

    # SUBREDDITS
    subreddits_where_subscirbed = OAUTH_URL + "/subreddits/mine/subscriber"
    subreddits_about = OAUTH_URL + "/r/{subreddit}/about"

    # POSTS
    search_posts_in_subreddit = OAUTH_URL + "/r/{subreddit}/search"

    # USERS
    user_about = OAUTH_URL + "/user/{username}/about"

    # SEARCH
    search = OAUTH_URL + "/search"


def encode_url(url: str, query_params: Dict[str, str]) -> str:
    return url + "?" + urllib.parse.urlencode(query_params)
