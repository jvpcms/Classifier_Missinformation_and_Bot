from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class User:
    id: str
    name: str
    display_name: str
    display_name_prefixed: str
    title: str
    description: str
    public_description: str
    subscribers: int
    url: str
    awardee_karma: int
    link_karma: int
    total_karma: int
    comment_karma: int
    created_utc: float

    @staticmethod
    def from_dict(response: Dict[str, Any]) -> "User":
        return User(
            id=response["data"]["id"],
            name=response["data"]["name"],
            display_name=response["data"]["subreddit"]["display_name"],
            display_name_prefixed=response["data"]["subreddit"][
                "display_name_prefixed"
            ],
            title=response["data"]["subreddit"]["title"],
            description=response["data"]["subreddit"]["description"],
            public_description=response["data"]["subreddit"]["public_description"],
            subscribers=response["data"]["subreddit"]["subscribers"],
            url=response["data"]["subreddit"]["url"],
            awardee_karma=response["data"]["awardee_karma"],
            link_karma=response["data"]["link_karma"],
            total_karma=response["data"]["total_karma"],
            comment_karma=response["data"]["comment_karma"],
            created_utc=response["data"]["created_utc"],
        )
