import os
import dotenv
from typing import Optional


class EnvConfig:
    def __init__(self) -> None:
        pass

    def _get_env(self, env_name: str, default: Optional[str] = None) -> str:
        dotenv.load_dotenv()
        env_var = os.getenv(env_name)

        if env_var is None:
            if default is not None:
                return default
            else:
                raise Exception(f"Envioriment variable {env_name} not set.")

        return env_var

    @property
    def logging_level(self) -> int:
        env_name = "LOGGING_LEVEL"
        env_var = self._get_env(env_name, "1")

        return int(env_var)

    @property
    def mongo_username(self) -> str:
        env_name = "MONGO_INITDB_ROOT_USERNAME"
        return self._get_env(env_name)

    @property
    def mongo_password(self) -> str:
        env_name = "MONGO_INITDB_ROOT_PASSWORD"
        return self._get_env(env_name)

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

    @property
    def language(self) -> str:
        env_name = "LANGUAGE"
        return self._get_env(env_name)

    @property
    def nltk_data_path(self) -> str:
        env_name = "NLTK_DATA_PATH"
        return self._get_env(env_name)


class Config:
    envs: EnvConfig

    def __init__(self):
        self.envs = EnvConfig()


def get_config():
    return Config()
