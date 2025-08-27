from datetime import datetime
from typing import Any, Dict, Union
from dataclasses import dataclass

from atproto_client.models.app.bsky.feed.defs import PostView
from dateutil.tz import gettz

from models.bluesky_user_model import BlueSkyUser
from models.labeled_news import LabeledNews


@dataclass
class BlueSkyPost:
    date_added: datetime
    news_link: Union[str, None]
    uri: str
    link: Union[str, None]
    user_did: str
    datetime: Union[datetime, None]
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
            news_link=None,
            link=None,
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

    def associate_with_labeled_news(self, labeled_news: LabeledNews) -> None:
        """Associate this post with a labeled news item."""

        self.news_link = labeled_news.link

    def associate_with_link(self, user: BlueSkyUser) -> None:
        """Associate this post with a specific link."""
        
        self.link = f"https://bsky.app/profile/{user.handle}/post/{self.rkey}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date_added": (
                self.date_added.timestamp() 
                if self.date_added is not None 
                else None
            ),
            "news_link": self.news_link,
            "uri": self.uri,
            "link": self.link,
            "datetime": (
                self.datetime.timestamp() 
                if self.datetime is not None 
                else None
            ),
            "text": self.text,
            "like_count": self.like_count,
            "repost_count": self.repost_count,
            "reply_count": self.reply_count,
            "quote_count": self.quote_count,
            "user_did": self.user_did,
            "langs": self.langs,
            "images": self.images,
        }

    @staticmethod
    def from_db_entry(entry: dict) -> "BlueSkyPost":
        return BlueSkyPost(
            date_added=datetime.fromtimestamp(entry["date_added"]),
            news_link=entry.get("news_link", None),
            uri=entry["uri"],
            link=entry.get("link", None),
            user_did=entry["user_did"],
            datetime=(
                datetime.fromtimestamp(entry["datetime"])
                if entry.get("datetime") is not None
                else None
            ),
            text=entry.get("text", None),
            like_count=entry.get("like_count", None),
            repost_count=entry.get("repost_count", None),
            reply_count=entry.get("reply_count", None),
            quote_count=entry.get("quote_count", None),
            langs=entry.get("langs", []) or [],
            images=entry.get("images", []) or [],
        )

    @property
    def rkey(self) -> str:
        """Return a unique key for this post."""
        return self.uri.split("/")[-1]
