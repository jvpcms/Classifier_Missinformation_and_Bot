from reddit_api.interfaces.factory import get_interfaces

__reddit_interfaces = get_interfaces()

postInterface = __reddit_interfaces.post_interface
subredditInterface = __reddit_interfaces.subreddit_interface
userInterface = __reddit_interfaces.user_interface
