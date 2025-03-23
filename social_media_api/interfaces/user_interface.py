from social_media_api.services.factory import Services
from social_media_api.services.reddit_client import RedditClient

from social_media_api.utils.factory import Utils
from social_media_api.utils.endpoints import Endpoints

from social_media_api.models.user_model import User


class UserInterface:
    client: RedditClient
    endpoints: Endpoints

    def __init__(self, services: Services, utils: Utils):
        self.client = services.reddit_client
        self.endpoints = utils.endpoints

    def about(self, username: str) -> User:
        url = self.endpoints.user_about.format(username=username)
        return self.client.api_call(url, User)
