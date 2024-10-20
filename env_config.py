import os
import dotenv


class EnvConfig:
    def __init__(self) -> None:
        pass

    @property
    def username(self) -> str:
        env_name = "REDDIT_USERNAME"
        dotenv.load_dotenv()
        env_var = os.getenv(env_name)

        if env_var is None:
            raise Exception(f"Envioriment variable {env_name} not set.")

        return env_var

    @property
    def password(self) -> str:
        env_name = "REDDIT_PASSWORD"
        dotenv.load_dotenv()
        env_var = os.getenv(env_name)

        if env_var is None:
            raise Exception(f"Envioriment variable {env_name} not set.")

        return env_var

    @property
    def app_id(self) -> str:
        env_name = "REDDIT_APP_ID"
        dotenv.load_dotenv()
        env_var = os.getenv(env_name)

        if env_var is None:
            raise Exception(f"Envioriment variable {env_name} not set.")

        return env_var

    @property
    def client_secret(self) -> str:
        env_name = "REDDIT_CLIENT_SECRET"
        dotenv.load_dotenv()
        env_var = os.getenv(env_name)

        if env_var is None:
            raise Exception(f"Envioriment variable {env_name} not set.")

        return env_var


# Instanciate class
envs = EnvConfig()
