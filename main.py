from interfaces.factory import get_interfaces
from repos.factory import get_repos


interfaces = get_interfaces()
post_interface = interfaces.post_interface

# repos = get_repos()
# post_repo = repos.posts
# post_repo.read_all()

posts = post_interface.search("Latest News", limit=1)
#
# for post in posts:
#     post_repo.insert(post)
