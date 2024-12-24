import os
import dotenv


class EnvConfig:
    def __init__(self) -> None:
        pass

    @property
    def mongo_username(self) -> str:
        env_name = "MONGO_INITDB_ROOT_USERNAME"
        dotenv.load_dotenv()
        env_var = os.getenv(env_name)

        if env_var is None:
            raise Exception(f"Envioriment variable {env_name} not set.")

        return env_var

    @property
    def mongo_password(self) -> str:
        env_name = "MONGO_INITDB_ROOT_PASSWORD"
        dotenv.load_dotenv()
        env_var = os.getenv(env_name)

        if env_var is None:
            raise Exception(f"Envioriment variable {env_name} not set.")

        return env_var
