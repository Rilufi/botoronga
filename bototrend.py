import praw
import tweepy
import random
from auth import client
import os
import re


def extract_hashtags_from_text(text):
    # Usa expressão regular para encontrar hashtags no texto
    hashtags = re.findall(r'#\w+', text)
    return hashtags

def extract_hashtags_from_post_content(post):
    # Extrai hashtags do conteúdo do post
    post_hashtags = extract_hashtags_from_text(post.selftext)
    return post_hashtags

def get_reddit_trending_topic():
    try:
        # Inicialize o objeto da API do Reddit
        reddit = praw.Reddit(
            client_id = os.environ.get("CLIENT_ID"),
            client_secret = os.environ.get("CLIENT_SECRET"),
            user_agent="GatobotScript")
      
        # Escolha um subreddit aleatório
        subreddit = reddit.random_subreddit()

        # Obtenha um tópico atual do subreddit selecionado
        trending_topic = random.choice(list(subreddit.top(limit=1)))

        return trending_topic
    except Exception as e:
        print(f"Erro ao obter o tópico em alta do Reddit: {e}")
        return None

if __name__ == "__main__":
    # Obtém o tópico em alta do Reddit
    trending_topic = get_reddit_trending_topic()

    if trending_topic:
        print(f"Tópico em alta do momento no Reddit:\n{trending_topic.title}")

        # Extrai hashtags relacionadas ao tópico do título e do conteúdo do post
        title_hashtags = extract_hashtags_from_text(trending_topic.title)
        post_content_hashtags = extract_hashtags_from_post_content(trending_topic)

        # Combina todas as hashtags
        all_hashtags = title_hashtags + post_content_hashtags

        # Filtra hashtags duplicadas
        unique_hashtags = list(set(all_hashtags))

        # Obtém o link para o tópico no Reddit
        reddit_link = f"https://www.reddit.com{trending_topic.permalink}"

        # Posta o tópico no Twitter
        tweet = f"""Tópico em alta do momento no Reddit:

{trending_topic.title} 

{' '.join(unique_hashtags)}

{reddit_link}"""
        
        client.create_tweet(text=tweet)
        print("Tópico postado no Twitter com sucesso!")
    else:
        print("Não foi possível obter o tópico em alta do Reddit.")
