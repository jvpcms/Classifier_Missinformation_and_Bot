from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client import RedditClient

from endpoints import Endpoints
from models.user_model import User


class UserInterface:
    def __init__(self, client: "RedditClient"):
        self.client = client

    def about(self, username: str) -> "_AboutUser":
        return _AboutUser(self.client, username)


class _AboutUser:
    def __init__(self, client: "RedditClient", username: str):
        self.client = client
        self.username = username

    def execute(self) -> User:
        url = Endpoints.user_about.format(username=self.username)

        result = self.client.execute(url, User)

        if isinstance(result, list):
            return result[0]

        return result
