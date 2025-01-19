# Fake News and Bot Account Classifier
## Setup

### Environment Variables
```
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_APP_ID=your_reddit_app_id
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
MONGO_INITDB_ROOT_USERNAME=db_username
MONGO_INITDB_ROOT_PASSWORD=db_password
```

## Components
### Reddit API
Esta aplicação em Python foi desenvolvida com o objetivo de simplificar e abstrair a comunicação com a API do Reddit, proporcionando uma interface organizada e orientada a objetos para interações com os dados da plataforma. Inspirada por um modelo de ORM (Object-Relational Mapping), a aplicação encapsula as requisições HTTP, permitindo que operações na API do Reddit sejam realizadas de maneira intuitiva, utilizando classes e objetos para representar posts, perfis de usuários, subreddits e outras entidades relevantes.

O desenvolvimento dessa aplicação é motivado pela necessidade de extrair dados de publicações de notícias e construir conjuntos de dados consistentes sobre notícias falsas e verdadeiras, para aplicações em inteligência artificial, como treinamento de modelos de classificação. Além disso, a aplicação permite a coleta de dados sobre perfis de usuários, possibilitando a análise e a classificação de contas como bots ou não-bots com base em suas atividades e características comportamentais.

### Database
### Web Scraping

## Basic Use
```python
  from interfaces.factory import get_interfaces


  interfaces = get_interfaces()

  # instantiate interfaces
  post_interface = interfaces.post_interface
  subreddit_interface = interfaces.subreddit_interface
  user_interface = interfaces.user_interface

  # search posts
  posts = post_interface.search("Latest News", limit=3)

  # user and subreddit details
  for post in posts:
      user = user_interface.about(post.author)
      subreddit = subreddit_interface.about(post.subreddit)
```
