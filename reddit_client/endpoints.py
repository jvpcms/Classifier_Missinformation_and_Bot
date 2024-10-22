URL = "https://www.reddit.com"
OAUTH_URL = "https://oauth.reddit.com"


class Endpoints:
    # AUTHENTICATION
    access_token = URL + "/api/v1/access_token"

    # ME
    me = OAUTH_URL + "/api/v1/me"

    # SUBREDDITS
    subreddits_where_subscirbed = OAUTH_URL + "/subreddits/mine/subscriber"
