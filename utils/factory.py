from env_config import EnvConfig
from endpoints import Endpoints
from parser import Parser


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
