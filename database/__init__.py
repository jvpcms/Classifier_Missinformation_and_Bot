from database.repos.factory import get_repos

__databaseRepos = get_repos()

postRepo = __databaseRepos.posts
userRepo = __databaseRepos.users
subredditRepo = __databaseRepos.subreddits
