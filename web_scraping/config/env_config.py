import os
import dotenv


class EnvConfig:
    def __init__(self) -> None:
        pass

    @property
    def language(self) -> str:
        env_name = "LANGUAGE"
        dotenv.load_dotenv()
        env_var = os.getenv(env_name)

        if env_var is None:
            raise Exception(f"Envioriment variable {env_name} not set.")

        return env_var

    @property
    def nltk_data_path(self) -> str:
        env_name = "NLTK_DATA_PATH"
        dotenv.load_dotenv()
        env_var = os.getenv(env_name)

        if env_var is None:
            raise Exception(f"Envioriment variable {env_name} not set.")

        return env_var
