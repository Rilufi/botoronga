import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.dates import DateFormatter, WeekdayLocator
from datetime import timedelta
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import tweepy
import os
import COVID19Py
from covid import Covid
import pandas
from auth import api
import io
from PIL import Image


# Step 1: Load the data
df = pd.read_csv(
    'https://covid.ourworldindata.org/data/owid-covid-data.csv',
    usecols=['date', 'location', 'total_vaccinations_per_hundred'],
    parse_dates=['date'])

countries = ['United States', 'Germany', 'United Kingdom', 'Brazil', 'Argentina', 'Chile', 'Uruguay']
df = df[df['location'].isin(countries)]



# Step 2: Summarize the data
pivot = pd.pivot_table(
    data=df,                                    # What dataframe to use
    index='date',                               # The "rows" of your dataframe
    columns='location',                         # What values to show as columns
    values='total_vaccinations_per_hundred',    # What values to aggregate
    aggfunc='mean',                             # How to aggregate data
    )

pivot = pivot.fillna(method='ffill')


# Step 3: Set up key variables for the visualization
main_country = 'Brazil'
colors = {country:('black' if country!= main_country else '#129583') for country in countries}
alphas = {country:(0.5 if country!= main_country else 1.0) for country in countries}


# Step 4: Plot all countries
fig, ax = plt.subplots(figsize=(12,8))
fig.patch.set_facecolor('#F5F5F5')    # Change background color to a light grey
ax.patch.set_facecolor('#F5F5F5')     # Change background color to a light grey

for country in countries:
    ax.plot(
        pivot.index,              # What to use as your x-values
        pivot[country],           # What to use as your y-values
        color=colors[country],    # How to color your line
        alpha=alphas[country]     # What transparency to use for your line
    )
    ax.text(
        x = pivot.index[-1] + timedelta(days=2),    # Where to position your text relative to the x-axis
        y = pivot[country].max(),                   # How high to position your text
        color = colors[country],
        fontsize=13,                   # What color to give your text
        s = country,                                # What to write
        alpha=alphas[country]                       # What transparency to use
    )


# Step 5: Configures axes
## A) Format what shows up on axes and how it's displayed
date_form = DateFormatter("%d-%m-%Y")
ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(0), interval=1))
ax.xaxis.set_major_formatter(date_form)
plt.xticks(rotation=45, fontsize=12)
#plt.ylim(0,100)

## B) Customizing axes and adding a grid
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#3f3f3f')
ax.spines['left'].set_color('#3f3f3f')
ax.tick_params(colors='#3f3f3f')
ax.grid(alpha=1)

## C) Adding a title and axis labels
plt.ylabel('Total de doses administradas por 100 pessoas', fontsize=18, alpha=0.9)
plt.xlabel('Date', fontsize=12, alpha=0.9)
plt.title('Vacinações COVID-19', fontsize=18, weight='bold', alpha=0.9)

# D) Celebrate!
plt.savefig("covid_vac")
