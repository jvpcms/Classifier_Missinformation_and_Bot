from datetime import datetime
from typing import Any, Dict, Union
from dataclasses import dataclass

from atproto_client.models.app.bsky.feed.defs import PostView
from dateutil.tz import gettz


@dataclass
class BlueSkyPost:
    date_added: datetime
    uri: str
    user_did: str
    datetime: datetime
    text: Union[str, None]
    like_count: Union[int, None]
    repost_count: Union[int, None]
    reply_count: Union[int, None]
    quote_count: Union[int, None]
    langs: list[str]
    images: list[str]

    @staticmethod
    def instantiate(post: PostView) -> "BlueSkyPost":
        return BlueSkyPost(
            date_added=datetime.now().astimezone(gettz("UTC")),
            uri=post.uri,
            user_did=post.author.did,
            datetime=datetime.fromisoformat(post.indexed_at.replace("Z", "+00:00")),
            text=getattr(post.record, "text", None),
            like_count=post.like_count,
            repost_count=post.repost_count,
            reply_count=post.reply_count,
            quote_count=post.quote_count,
            langs=getattr(post.record, "langs", []) or [],
            images=[
                image.fullsize for image in getattr(post.embed, "images", []) or []
            ],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date_added": self.date_added,
            "uri": self.uri,
            "datetime": self.datetime,
            "text": self.text,
            "like_count": self.like_count,
            "repost_count": self.repost_count,
            "reply_count": self.reply_count,
            "quote_count": self.quote_count,
            "user_did": self.user_did,
            "langs": self.langs,
            "images": self.images,
        }
