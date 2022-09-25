import tweepy
import os
import pandas as pd
from datetime import date, timedelta, datetime
from auth import api


# Data de ontem

today = date.today()
yesterday = today - timedelta(days=1)
yesterday = str(yesterday)

# Database do owid

df = pd.read_csv(
    'https://covid.ourworldindata.org/data/owid-covid-data.csv')

loc = df['location']
date = df['date']

# Dados BR

br_info = df[(loc == 'Brazil') & (date == yesterday)]

try:
    confirmed = int(br_info['total_cases'])
    confirmed_24 = int(br_info['new_cases'])
    deaths = int(br_info['total_deaths'])
    deaths_24 = int(br_info['new_deaths'])

    mystring_br = f"""#COVID-19 no Brasil

    Casos confirmados: {confirmed:,}
    Casos em 24h: {confirmed_24:,}
    Total de mortes: {deaths:,}
    Mortes em 24h: {deaths_24:,}

    Fonte: https://covid.ourworldindata.org"""

    api.update_status(mystring_br)
    
    # Dados EUA

    us_info = df[(loc == 'United States') & (date == yesterday)]

    confirmed = int(us_info['total_cases'])
    confirmed_24 = int(us_info['new_cases'])
    deaths = int(us_info['total_deaths'])
    deaths_24 = int(us_info['new_deaths'])

    mystring_us = f""" COVID-19 nos EUA

    Casos confirmados: {confirmed:,}
    Casos em 24h: {confirmed_24:,}
    Total de mortes: {deaths:,}
    Mortes em 24h: {deaths_24:,}

    Fonte: https://covid.ourworldindata.org"""


    # Find the last tweet and reply

    toReply = api.me().screen_name

    tweets = api.user_timeline(screen_name = toReply, count=1)

    for tweet in tweets:
            api.update_status("@" + toReply + mystring_us, in_reply_to_status_id = tweet.id)

except ValueError:
    confirmed = int(br_info['total_cases'])
    confirmed_24 = 0
    deaths = int(br_info['total_deaths'])
    deaths_24 = 0

    mystring_br = f"""#COVID-19 no Brasil

    Casos confirmados: {confirmed:,}
    Casos em 24h: {confirmed_24:,}
    Total de mortes: {deaths:,}
    Mortes em 24h: {deaths_24:,}

    Fonte: https://covid.ourworldindata.org"""

    api.update_status(mystring_br)
    
    # Dados EUA

    us_info = df[(loc == 'United States') & (date == yesterday)]

    confirmed = int(us_info['total_cases'])
    deaths = int(us_info['total_deaths'])

    mystring_us = f""" COVID-19 nos EUA

    Casos confirmados: {confirmed:,}
    Casos em 24h: {confirmed_24:,}
    Total de mortes: {deaths:,}
    Mortes em 24h: {deaths_24:,}

    Fonte: https://covid.ourworldindata.org"""


    # Find the last tweet and reply

    toReply = api.me().screen_name

    tweets = api.user_timeline(screen_name = toReply, count=1)

    for tweet in tweets:
            api.update_status("@" + toReply + mystring_us, in_reply_to_status_id = tweet.id)



# Dados Mundo

wrl_info = df[(loc == 'World') & (date == yesterday)]

confirmed = int(wrl_info['total_cases'])
confirmed_24 = int(wrl_info['new_cases'])
deaths = int(wrl_info['total_deaths'])
deaths_24 = int(wrl_info['new_deaths'])

mystring_wrl = f""" COVID-19 no Mundo

Casos confirmados: {confirmed:,}
Casos em 24h: {confirmed_24:,}
Total de mortes: {deaths:,}
Mortes em 24h: {deaths_24:,}

Fonte: https://covid.ourworldindata.org"""

tweets = api.user_timeline(screen_name = toReply, count=1)

for tweet in tweets:
        api.update_status("@" + toReply + mystring_wrl, in_reply_to_status_id = tweet.id)



#### Gráficos
### Gráfico de Vacina/centena

tweets = api.user_timeline(screen_name = toReply, count=1)

mystring_vac = """ Vacinações por Centena pelo Mundo

Dados relacionados ao total de doses administradas.

Fonte: https://covid.ourworldindata.org/"""

for tweet in tweets:
        api.update_with_media('data/covid_vac.png', "@" + toReply + mystring_vac, in_reply_to_status_id = tweet.id)


### Gráfico de porcentagem

mystring_vacbr = f""" Vacinações por Milhão pelo Mundo

Dados relacionados à pessoas vacinadas com pelo menos uma dose.

Fonte: https://covid.ourworldindata.org/"""

tweets = api.user_timeline(screen_name = toReply, count=1)

for tweet in tweets:
        api.update_with_media('data/covid_vactot.png', "@" + toReply + mystring_vacbr, in_reply_to_status_id = tweet.id)


### Gráfico de Casos Mundo

tweets = api.user_timeline(screen_name = toReply, count=1)

mystring_vac = """ Novos Casos Diários Confirmados no Mundo

Fonte: https://covid.ourworldindata.org"""

for tweet in tweets:
        api.update_with_media('data/world_cases.png', "@" + toReply + mystring_vac, in_reply_to_status_id = tweet.id)


### Gráfico de Casos BR

tweets = api.user_timeline(screen_name = toReply, count=1)

mystring_vac = """ Novos Casos Diários Confirmados no Brasil

Fonte: https://covid.ourworldindata.org"""

for tweet in tweets:
        api.update_with_media('data/br_cases.png', "@" + toReply + mystring_vac, in_reply_to_status_id = tweet.id)



### Gráfico de Casos EUA, BR, FR

tweets = api.user_timeline(screen_name = toReply, count=1)

mystring_vac = """ Novos Casos Diários Confirmados no Brasil, EUA e França

Fonte: https://covid.ourworldindata.org"""

for tweet in tweets:
        api.update_with_media('data/covid_ind_cases.png', "@" + toReply + mystring_vac, in_reply_to_status_id = tweet.id)



### Gráfico de Mortes 24h Mundo

tweets = api.user_timeline(screen_name = toReply, count=1)

mystring_vac = """ Mortes em 24h no Mundo

Fonte: https://covid.ourworldindata.org"""

for tweet in tweets:
        api.update_with_media('data/world_deaths.png', "@" + toReply + mystring_vac, in_reply_to_status_id = tweet.id)


### Gráfico de Mortes 24h Brasil

tweets = api.user_timeline(screen_name = toReply, count=1)

mystring_vac = """ Mortes em 24h no Brasil

Fonte: https://covid.ourworldindata.org"""

for tweet in tweets:
        api.update_with_media('data/br_deaths.png', "@" + toReply + mystring_vac, in_reply_to_status_id = tweet.id)



### Gráfico de Mortes 24h Brasil, EUA e França

tweets = api.user_timeline(screen_name = toReply, count=1)

mystring_vac = """ Mortes em 24h no Brasil, EUA e França

Fonte: https://covid.ourworldindata.org"""

for tweet in tweets:
        api.update_with_media('data/covid_ind_deaths.png', "@" + toReply + mystring_vac, in_reply_to_status_id = tweet.id)


### Gráfico de Mortes Total EUA


tweets = api.user_timeline(screen_name = toReply, count=1)

mystring_vac = """ Total de Mortes no Brasil e nos EUA

Fonte: https://covid.ourworldindata.org"""

for tweet in tweets:
        api.update_with_media('data/covid_ind_totdeaths.png', "@" + toReply + mystring_vac, in_reply_to_status_id = tweet.id)


### Gráfico de Mortes Total Mundo


tweets = api.user_timeline(screen_name = toReply, count=1)

mystring_vac = """ Total de Mortes no Mundo

Fonte: https://covid.ourworldindata.org"""

for tweet in tweets:
        api.update_with_media('data/world_totdeaths.png', "@" + toReply + mystring_vac, in_reply_to_status_id = tweet.id)
