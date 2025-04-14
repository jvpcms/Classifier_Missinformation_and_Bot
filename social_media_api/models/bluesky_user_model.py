from datetime import datetime
from dateutil.tz import gettz
from dataclasses import dataclass
from typing import Any, Dict, Union

from atproto_client.models.app.bsky.actor.defs import ProfileViewDetailed


@dataclass
class BlueSkyUser:
    date_added: datetime
    did: str
    handle: str
    about: Union[str, None]
    datetime: Union[datetime, None]
    display_name: Union[str, None]
    followers_count: Union[int, None]
    follows_count: Union[int, None]
    posts_count: Union[int, None]

    @staticmethod
    def instantiate(profile: ProfileViewDetailed) -> "BlueSkyUser":
        return BlueSkyUser(
            date_added=datetime.now().astimezone(gettz("UTC")),
            did=profile.did,
            handle=profile.handle,
            about=profile.description,
            datetime=(
                datetime.fromisoformat(profile.indexed_at.replace("Z", "+00:00"))
                if profile.indexed_at is not None
                else None
            ),
            display_name=profile.display_name,
            followers_count=profile.followers_count,
            follows_count=profile.follows_count,
            posts_count=profile.posts_count,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "datea_added": self.date_added,
            "did": self.did,
            "handle": self.handle,
            "about": self.about,
            "datetime": self.datetime,
            "display_name": self.display_name,
            "followers_count": self.followers_count,
            "follows_count": self.follows_count,
            "posts_count": self.posts_count,
        }
