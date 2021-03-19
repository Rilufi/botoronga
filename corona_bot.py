# coding=utf-8

import tweepy
import os
import COVID19Py
from covid import Covid
import pandas
from credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

covid = Covid()
br_cases = covid.get_status_by_country_id(24)

confirmed = (br_cases.get('confirmed'))
deaths = (br_cases.get('deaths'))
active= (br_cases.get('active'))

df = pandas.read_csv('all_dead.csv')
mortos = int(df.values[0])
all_dead = deaths - mortos
df.at[0,"Mortos"] = deaths
df.to_csv('all_dead.csv', index=False)

mystring = f"""COVID-19 no Brasil

Casos confirmados: {confirmed:,}
Mortes: {deaths:,}
Mortes em 24h: {all_dead:,}
Confirmados ativos: {active:,}

Fonte: https://systems.jhu.edu/research/public-health/ncov/"""

api.update_status(mystring)

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

    toReply = "user" #user to get most recent tweet

    tweets = api.user_timeline(screen_name = toReply, count=1)

    for tweet in tweets:
        api.update_status("@" + toReply + mystring_all, in_reply_to_status_id = tweet.id)

except:
    pass
