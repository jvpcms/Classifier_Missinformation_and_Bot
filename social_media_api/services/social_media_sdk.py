from abc import ABC, abstractmethod
from social_media_api.utils.factory import Utils, get_utils
from social_media_api.config.factory import Config, get_config


class SocialMediaSdk(ABC):
    def __init__(self, config: Config, utils: Utils):
        raise NotImplementedError

    @abstractmethod
    def search_posts(self, query: str):
        """Search posts in the social media platform"""

    @abstractmethod
    def search_users(self, query: str):
        """Search users in the social media platform"""

    @abstractmethod
    def get_post_details(self, post_id: str):
        """Get post details in the social media platform"""

    @abstractmethod
    def get_user_details(self, user_id: str):
        """Get user details in the social media platform"""
