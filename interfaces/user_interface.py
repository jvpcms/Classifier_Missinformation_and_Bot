from services.factory import Services
from utils.factory import Utils

from models.user_model import User


class UserInterface:
    def __init__(self, services: Services, utils: Utils):
        self.client = services.reddit_client
        self.endpoints = utils.endpoints

    def about(self, username: str) -> User:
        url = self.endpoints.user_about.format(username=username)
        return self.client.execute(url, User)
