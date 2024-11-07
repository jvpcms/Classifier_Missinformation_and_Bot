from utils.env_config import EnvConfig
from utils.endpoints import Endpoints
from utils.parser import Parser


class Utils:
    envs: EnvConfig
    parser: Parser
    endpoints: Endpoints

    def __init__(self):
        self.envs = EnvConfig()
        self.parser = Parser()
        self.endpoints = Endpoints()


def get_utils():
    return Utils()
