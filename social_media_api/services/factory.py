from social_media_api.utils.factory import Utils, get_utils
from social_media_api.config.factory import Config, get_config

from social_media_api.services.social_media_sdk import (
    SocialMediaSdk,
    BlueSkySdk,
    RedditSdk,
)

from social_media_api.models.bluesky_post_model import BlueSkyPost
from social_media_api.models.bluesky_user_model import BlueSkyUser
from social_media_api.models.reddit_post_model import RedditPost
from social_media_api.models.reddit_user_model import RedditUser


class Services:
    reddit_sdk: SocialMediaSdk[RedditPost, RedditUser]
    bluesky_sdk: SocialMediaSdk[BlueSkyPost, BlueSkyUser]

    def __init__(self, config: Config, utils: Utils):
        self.reddit_sdk = RedditSdk(config, utils)
        self.bluesky_sdk = BlueSkySdk(config, utils)


def get_services():
    utils = get_utils()
    config = get_config()

    return Services(config, utils)
