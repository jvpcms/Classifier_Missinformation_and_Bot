import os
import dotenv


class EnvConfig:
    def __init__(self) -> None:
        pass

    def _get_env(self, env_name: str) -> str:
        dotenv.load_dotenv()
        env_var = os.getenv(env_name)

        if env_var is None:
            raise Exception(f"Envioriment variable {env_name} not set.")

        return env_var

    @property
    def username(self) -> str:
        env_name = "REDDIT_USERNAME"
        return self._get_env(env_name)

    @property
    def password(self) -> str:
        env_name = "REDDIT_PASSWORD"
        return self._get_env(env_name)

    @property
    def app_id(self) -> str:
        env_name = "REDDIT_APP_ID"
        return self._get_env(env_name)

    @property
    def client_secret(self) -> str:
        env_name = "REDDIT_CLIENT_SECRET"
        return self._get_env(env_name)

    @property
    def bluesky_username(self) -> str:
        env_name = "BLUESKY_USERNAME"
        return self._get_env(env_name)

    @property
    def bluesky_secret(self) -> str:
        env_name = "BLUESKY_SECRET"
        return self._get_env(env_name)
