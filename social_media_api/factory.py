from config.envconfig import Config, get_config

from social_media_api.social_media_sdk import (
    SocialMediaSdk,
    BlueSkySdk,
    RedditSdk,
)

from models.bluesky_post_model import BlueSkyPost
from models.bluesky_user_model import BlueSkyUser
from models.reddit_post_model import RedditPost
from models.reddit_user_model import RedditUser


class Socialmediasdkcollection:
    reddit_sdk: SocialMediaSdk[RedditPost, RedditUser]
    bluesky_sdk: SocialMediaSdk[BlueSkyPost, BlueSkyUser]

    def __init__(self, config: Config):
        self.reddit_sdk = RedditSdk(config)
        self.bluesky_sdk = BlueSkySdk(config)


def get_social_media_sdk_colleciton():
    config = get_config()

    return Socialmediasdkcollection(config)
