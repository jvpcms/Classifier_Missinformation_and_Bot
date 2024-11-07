from env_config import EnvConfig
from endpoints import Endpoints
from parser import Parser


class Utils:
    envs: EnvConfig
    parser: Parser
    endpoints: Endpoints

    def __init__(self, envs: EnvConfig, parser: Parser, endpoints: Endpoints):
        self.envs = envs
        self.parser = parser
        self.endpoints = endpoints


def get_utils():
    envs = EnvConfig()
    parser = Parser()
    endpoints = Endpoints()

    return Utils(envs, parser, endpoints)
