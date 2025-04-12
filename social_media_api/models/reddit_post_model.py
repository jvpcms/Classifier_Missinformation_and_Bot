from datetime import datetime
from dateutil.tz import tzutc
from typing import Any, Dict
from dataclasses import dataclass


@dataclass
class RedditPost:
    id: str
    subreddit: str
    subreddit_name_prefixed: str
    subreddit_id: str
    subreddit_subscribers: int
    author: str
    author_fullname: str
    title: str
    selftext: str
    name: str
    upvote_ratio: float
    ups: int
    score: int
    is_original_content: bool
    link_flair_text: str
    created_utc: datetime
    media_only: bool
    media: Dict[str, Any]
    num_comments: int
    permalink: str
    url: str
    num_crossposts: int
    is_video: bool

    @staticmethod
    def from_dict(response: Dict[str, Any]) -> "RedditPost":
        return RedditPost(
            id=response["data"]["id"],
            subreddit=response["data"]["subreddit"],
            subreddit_name_prefixed=response["data"]["subreddit_name_prefixed"],
            subreddit_id=response["data"]["subreddit_id"],
            subreddit_subscribers=response["data"]["subreddit_subscribers"],
            author=response["data"]["author"],
            author_fullname=response["data"]["author_fullname"],
            title=response["data"]["title"],
            selftext=response["data"]["selftext"],
            name=response["data"]["name"],
            upvote_ratio=response["data"]["upvote_ratio"],
            ups=response["data"]["ups"],
            score=response["data"]["score"],
            is_original_content=response["data"]["is_original_content"],
            link_flair_text=response["data"]["link_flair_text"],
            created_utc=datetime.fromtimestamp(
                response["data"]["created_utc"], tz=tzutc()
            ),
            media_only=response["data"]["media_only"],
            media=response["data"]["media"],
            num_comments=response["data"]["num_comments"],
            permalink=response["data"]["permalink"],
            url=response["data"]["url"],
            num_crossposts=response["data"]["num_crossposts"],
            is_video=response["data"]["is_video"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "subreddit": self.subreddit,
            "subreddit_name_prefixed": self.subreddit_name_prefixed,
            "subreddit_id": self.subreddit_id,
            "subreddit_subscribers": self.subreddit_subscribers,
            "author": self.author,
            "author_fullname": self.author_fullname,
            "title": self.title,
            "selftext": self.selftext,
            "name": self.name,
            "upvote_ratio": self.upvote_ratio,
            "ups": self.ups,
            "score": self.score,
            "is_original_content": self.is_original_content,
            "link_flair_text": self.link_flair_text,
            "created_utc": self.created_utc.timestamp(),
            "media_only": self.media_only,
            "media": self.media,
            "num_comments": self.num_comments,
            "permalink": self.permalink,
            "url": self.url,
            "num_crossposts": self.num_crossposts,
            "is_video": self.is_video,
        }
