from config.env_config import EnvConfig


class Config:
    envs: EnvConfig

    def __init__(self):
        self.envs = EnvConfig()


def get_config():
    return Config()
