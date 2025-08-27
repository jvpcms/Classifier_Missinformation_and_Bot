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
            "datea_added": self.date_added.timestamp(),
            "did": self.did,
            "handle": self.handle,
            "about": self.about,
            "datetime": (
                self.datetime.timestamp() if self.datetime is not None else None
            ),
            "display_name": self.display_name,
            "followers_count": self.followers_count,
            "follows_count": self.follows_count,
            "posts_count": self.posts_count,
        }

    @staticmethod
    def from_db_entry(entry: dict) -> "BlueSkyUser":
        return BlueSkyUser(
            date_added=datetime.fromtimestamp(entry["datea_added"]).astimezone(
                gettz("UTC")
            ),
            did=entry["did"],
            handle=entry["handle"],
            about=entry.get("about"),
            datetime=(
                datetime.fromtimestamp(entry["datetime"]).astimezone(gettz("UTC"))
                if entry.get("datetime") is not None
                else None
            ),
            display_name=entry.get("display_name"),
            followers_count=entry.get("followers_count"),
            follows_count=entry.get("follows_count"),
            posts_count=entry.get("posts_count"),
        )
