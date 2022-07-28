#! /usr/bin/env python
# coding=utf-8

import tweepy
import os
import COVID19Py
from covid import Covid
import pandas
from auth import api

covid = Covid()
br_cases = covid.get_status_by_country_id(24)

confirmed = (br_cases.get('confirmed'))
deaths = (br_cases.get('deaths'))
active= (br_cases.get('active'))

df = pandas.read_csv('all_dead.csv')
mortos = int(df.values[0][0])
all_dead = deaths - mortos
df.at[0,"Mortos"] = deaths
df.to_csv('all_dead.csv', index=False)

mystring = f"""COVID-19 no Brasil

Casos confirmados: {confirmed:,}
Mortes: {deaths:,}
Confirmados ativos: {active:,}

Fonte: https://ahmednafies.github.io/covid/john_hopkins/"""

#Mortes em 24h: {all_dead:,}

api.update_status(mystring)

toReply = api.me().screen_name

### Gráfico de Vacina/centena

tweets = api.user_timeline(screen_name = toReply, count=1)

mystring_vac = """ Vacinações por Centena pelo Mundo

Dados relacionados ao total de doses administradas.

Fonte: https://covid.ourworldindata.org/"""

for tweet in tweets:
        api.update_with_media('covid_vac.png', "@" + toReply + mystring_vac, in_reply_to_status_id = tweet.id)


### Gráfico de porcentagem

df = pandas.read_csv('all_dead.csv')
percent = float(df.values[1][0])
vacs = int(df.values[2][0])

mystring_vacbr = f""" Total de Brasileiros Vacinados: {vacs:,}

Porcentagem de Brasileiros Vacinados: {percent}%


Dados relacionados à pessoas vacinadas com pelo menos uma dose."""

tweets = api.user_timeline(screen_name = toReply, count=1)

for tweet in tweets:
        api.update_with_media('covid_vactot.png', "@" + toReply + mystring_vacbr, in_reply_to_status_id = tweet.id)


### Gráfico de Casos India

tweets = api.user_timeline(screen_name = toReply, count=1)

mystring_vac = """ Novos Casos Diários Confirmados no Brasil e na Índia
"""

for tweet in tweets:
        api.update_with_media('covid_ind_cases.png', "@" + toReply + mystring_vac, in_reply_to_status_id = tweet.id)


### Gráfico de Mortes 24h India

tweets = api.user_timeline(screen_name = toReply, count=1)

mystring_vac = """ Mortes em 24h no Brasil e na Índia
"""

for tweet in tweets:
        api.update_with_media('covid_ind_deaths.png', "@" + toReply + mystring_vac, in_reply_to_status_id = tweet.id)


### Gráfico de Mortes Total India


tweets = api.user_timeline(screen_name = toReply, count=1)

mystring_vac = """ Total de Mortes no Brasil e na Índia
"""

for tweet in tweets:
        api.update_with_media('covid_ind_totdeaths.png', "@" + toReply + mystring_vac, in_reply_to_status_id = tweet.id)


try:
    covid19 = COVID19Py.COVID19(data_source="jhu")

    latest = covid19.getLatest()

    location_us = covid19.getLocationByCountryCode("US")
    items_us = location_us[0].get('latest')

    confirmed_all = (latest.get('confirmed'))
    deaths_all = (latest.get('deaths'))

    confirmed_us = (items_us.get('confirmed'))
    deaths_us = (items_us.get('deaths'))

    mystring_all = f""" COVID-19 no mundo

Casos confirmados: {confirmed_all:,}
Mortes: {deaths_all:,}

COVID-19 nos EUA

Casos confirmados: {confirmed_us:,}
Mortes: {deaths_us:,}

Fonte: https://systems.jhu.edu/research/public-health/ncov/"""

    tweets = api.user_timeline(screen_name = toReply, count=1)

    for tweet in tweets:
        api.update_status("@" + toReply + mystring_all, in_reply_to_status_id = tweet.id)

except:
    pass
