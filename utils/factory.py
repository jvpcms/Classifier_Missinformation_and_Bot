from utils.endpoints import Endpoints
from utils.parser import Parser


class Utils:
    parser: Parser
    endpoints: Endpoints

    def __init__(self):
        self.parser = Parser()
        self.endpoints = Endpoints()


def get_utils():
    return Utils()
