import tweepy
import pandas as pd
import json
import sqlite3
import urllib.request
import ssl
from tweepy import OAuthHandler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

consumer_key="0V4yepQ23LtiYGLkhCzgRTQTO"
consumer_secret="JY7EtLqyDkSNueh9yvwMtMFMh8c4ozZPGNkaxggOYAhESu8TTs"
access_token="1447500735814402050-BQlfz2PdZIXrwuU7kCSwCZYKxyzahH"
access_token_secret="0ttrlWD85PBWBmsfBz7grrYJEDU8kvvYOsjJWezORCfak"

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)
search_words = ("#Coronavirus", "Vaccination")

keywords = tweepy.Cursor(api.search_tweets, q=search_words, lang="en").items(500)

#for i in keywords:
  #       print(i._json)

Comments={'score':[],'Date':[], 'Location':[]}


for i in keywords:
                   Comments['Date'].append(i._json['created_at'])
                   Comments['Location'].append(i._json['user']['location'])
                   vader=SentimentIntensityAnalyzer()
                   sentiment = vader.polarity_scores(i.text)
                   if sentiment['neg']>sentiment['pos'] and sentiment['neg']>sentiment['neu']:
                                                       Comments['score'].append('Bad')
                   elif sentiment['pos']>sentiment['neg'] and sentiment['pos']>sentiment['neu']:
                                                       Comments['score'].append('Good')
                   else :
                                                       Comments['score'].append('Neutral')



pd.options.display.max_colwidth = 200
df=pd.DataFrame(Comments)
print(df)

db = sqlite3.connect("C:\\Users\\genhk\\Shawn_ProjTwitter\\data.db")
c = db.cursor()
c.execute('''CREATE TABLE if not exists Rating
               (score text, date text, location text);''')

df.to_sql('Rating', db, if_exists='append', index=False)

db.commit()






