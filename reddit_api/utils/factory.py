from reddit_api.utils.endpoints import Endpoints
from reddit_api.utils.parser import Parser


class Utils:
    parser: Parser
    endpoints: Endpoints

    def __init__(self):
        self.parser = Parser()
        self.endpoints = Endpoints()


def get_utils():
    return Utils()
