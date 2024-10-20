import requests
import requests.auth
import shelve
from endpoints import Endpoints
from env_config import envs


class RedditClient:
    def __init__(self):
        self.username: str = envs.username
        self.password: str = envs.password
        self.app_id: str = envs.app_id
        self.client_secret: str = envs.client_secret

        self.store_path: str = "shelve/local_storage"

    def authenticate(self):
        """Authencation requests, store access token"""

        client_auth = requests.auth.HTTPBasicAuth(self.app_id, self.client_secret)

        post_data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
        }

        headers = {"User-Agent": f"ChangeMeClient/0.1 by {self.username}"}

        response = requests.post(
            Endpoints.access_token, auth=client_auth, data=post_data, headers=headers
        )

        if response.status_code != 200:
            raise Exception("Authencation failed")

        with shelve.open(self.store_path) as ls:
            ls["authentication_info"] = response.json()


if __name__ == "__main__":
    client = RedditClient()
    client.authenticate()

    with shelve.open(client.store_path) as ls:
        print(ls["authentication_info"])
