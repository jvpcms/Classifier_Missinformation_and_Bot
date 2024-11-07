from typing import Any, Dict, List, Type, TypeVar, Union, overload
from models.subreddit_model import Subreddit
from models.post_model import Post
from models.user_model import User


ModelType = TypeVar("ModelType", Subreddit, Post, User)


class Parser:
    @staticmethod
    @overload
    def parse(response: Dict[str, Any], model: Type[ModelType]) -> ModelType: ...

    @staticmethod
    @overload
    def parse(
        response: Dict[str, Any], model: Type[ModelType], *, many: bool
    ) -> List[ModelType]: ...

    @staticmethod
    def parse(
        response: Dict[str, Any], model: Type[ModelType], *, many: bool = False
    ) -> Union[ModelType, List[ModelType]]:
        """Parse API response into class intance(s)"""

        if not hasattr(model, "from_dict"):
            raise ValueError(f"{model} does not have a from_dict method")

        if many:
            children = response["data"]["children"]
            return [model.from_dict(child) for child in children]

        return model.from_dict(response)
