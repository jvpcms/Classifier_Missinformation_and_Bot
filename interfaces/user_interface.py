from services.factory import Services
from services.reddit_client import RedditClient

from utils.factory import Utils
from utils.endpoints import Endpoints

from models.user_model import User


class UserInterface:
    client: RedditClient
    endpoints: Endpoints

    def __init__(self, services: Services, utils: Utils):
        self.client = services.reddit_client
        self.endpoints = utils.endpoints

    def about(self, username: str) -> User:
        url = self.endpoints.user_about.format(username=username)
        return self.client.api_call(url, User)
