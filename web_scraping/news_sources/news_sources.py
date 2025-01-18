from abc import ABC
from typing import Literal


class NewsSource(ABC):
    url: str
    source_type: Literal["virtual_media", "checking_agency"]

    def __init__(self):
        raise NotImplementedError("This class is not meant to be instantiated")


class VirtualMedia(NewsSource):
    def __init__(self, url: str):
        self.source_type = "virtual_media"
        self.url = url


class CheckingAgency(NewsSource):
    def __init__(self, url: str):
        self.source_type = "checking_agency"
        self.url = url
