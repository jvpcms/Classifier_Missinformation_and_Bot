from interfaces.factory import get_interfaces


interfaces = get_interfaces()
post_interface = interfaces.post_interface
subreddit_interface = interfaces.subreddit_interface
user_interface = interfaces.user_interface

posts = post_interface.search("Latest News", limit=3)
print(posts)

for post in posts:
    user = user_interface.about(post.author)
    subreddit = subreddit_interface.about(post.subreddit)
