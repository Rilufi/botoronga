import praw
import tweepy
import random
from auth import client
import os
import re


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

def generate_hashtags(text, num_hashtags=3):
    # Remove caracteres especiais e converte o texto para letras minúsculas
    text = re.sub(r'[^\w\s]', '', text.lower())
    # Divide o texto em palavras
    words = text.split()
    # Remove palavras comuns
    common_words = {'the', 'and', 'but', 'with', 'for', 'from', 'in', 'on', 'of', 'at', 'a', 'an', 'is', 'are', 'were', 'was', 'to', 'that', 'this', 'it', 'you', 'he', 'she', 'they', 'we', 'i', 'or', 'not', 'as', 'if', 'has', 'have', 'been', 'be', 'do', 'does', 'did'}
    words = [word for word in words if word not in common_words]
    # Conta a frequência das palavras
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    # Ordena as palavras por frequência
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    # Seleciona as palavras mais frequentes como hashtags
    hashtags = ['#' + word for word, freq in sorted_words[:num_hashtags]]
    return hashtags

if __name__ == "__main__":
    # Obtém o tópico em alta do Reddit
    trending_topic = get_reddit_trending_topic()

    if trending_topic:
        print(f"Tópico em alta do momento no Reddit:\n{trending_topic.title}")

        # Gera hashtags relacionadas ao tópico do título e do conteúdo do post
        title_hashtags = generate_hashtags(trending_topic.title)
        print("Hashtags do título:", title_hashtags)

        post_content_hashtags = generate_hashtags(trending_topic.selftext)
        print("Hashtags do conteúdo do post:", post_content_hashtags)

        # Combina todas as hashtags
        all_hashtags = title_hashtags + post_content_hashtags
        print("Todas as hashtags:", all_hashtags)

        # Filtra hashtags duplicadas
        unique_hashtags = list(set(all_hashtags))
        print("Hashtags únicas:", unique_hashtags)

        # Obtém o link para o tópico no Reddit
        reddit_link = f"https://www.reddit.com{trending_topic.permalink}"

        # Posta o tópico no Twitter
        tweet = f"""Tópico em alta do momento no Reddit:

{trending_topic.title}

{' '.join(unique_hashtags)}

{reddit_link}"""
        print(tweet)
        client.create_tweet(text=tweet)
        print("Tópico postado no Twitter com sucesso!")
    else:
        print("Não foi possível obter o tópico em alta do Reddit.")
