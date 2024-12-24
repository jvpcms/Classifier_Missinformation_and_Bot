from reddit_api.services.factory import Services, get_services
from reddit_api.utils.factory import Utils, get_utils

from reddit_api.interfaces.post_interface import PostInterface
from reddit_api.interfaces.subreddit_interface import SubredditInterface
from reddit_api.interfaces.user_interface import UserInterface


class Interfaces:
    post_interface: PostInterface
    subreddit_interface: SubredditInterface
    user_interface: UserInterface

    def __init__(self, services: Services, utils: Utils):
        self.post_interface = PostInterface(services, utils)
        self.subreddit_interface = SubredditInterface(services, utils)
        self.user_interface = UserInterface(services, utils)


def get_interfaces():
    services = get_services()
    utils = get_utils()

    return Interfaces(services, utils)
