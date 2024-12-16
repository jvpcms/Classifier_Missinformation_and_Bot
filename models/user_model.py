from datetime import datetime
from dateutil.tz import tzutc
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
    created_utc: datetime

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
            created_utc=datetime.fromtimestamp(
                response["data"]["created_utc"], tz=tzutc()
            ),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "display_name_prefixed": self.display_name_prefixed,
            "title": self.title,
            "description": self.description,
            "public_description": self.public_description,
            "subscribers": self.subscribers,
            "url": self.url,
            "awardee_karma": self.awardee_karma,
            "link_karma": self.link_karma,
            "total_karma": self.total_karma,
            "comment_karma": self.comment_karma,
            "created_utc": self.created_utc.timestamp(),
        }
