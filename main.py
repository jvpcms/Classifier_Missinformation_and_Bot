from database import postRepo
from reddit_api import postInterface


posts = postInterface.search("Latest News", limit=1)
print(posts)

postRepo.read_all()
