import tweepy
import pandas as pd
import nltk
import textblob
import bs4
from unidecode import unidecode
import datetime
import numpy as np
import os

def get_parameters():
    params_list = []
    with open('get_tweets_config.txt', 'r') as params_txt:
        for row in params_txt:
            params_list.append(row.split('=')[-1].strip())
        
    return params_list

search_for, my_api_key, my_api_secret = get_parameters()

# authenticate
auth = tweepy.OAuthHandler(my_api_key, my_api_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

api = tweepy.API(auth)

def get_tweets(search_for):
    tweets = api.search_tweets(q=search_for, lang='pt-BR', count=500)
    tweets_copy = []
    for tweet in tweets:
        tweets_copy.append(tweet)
        
    print("Searching for tweets of:", search_for)

    tweets_df = pd.DataFrame()

    i = 0
    # populate the dataframe
    for tweet in tweets_copy:
        hashtags = []
        try:
            for hashtag in tweet.entities["hashtags"]:
                hashtags.append(hashtag["text"])
            text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
        except:
            pass
        tweets_df = pd.concat([tweets_df, pd.DataFrame({'user_name': tweet.user.name, 
                                                'user_location': tweet.user.location,\
                                                #'user_description': tweet.user.description,
                                                #'user_verified': tweet.user.verified,
                                                'date': tweet.created_at,
                                                'text': text,
                                                'rating': float('nan')
                                                #'hashtags': [hashtags if hashtags else None],
                                                #'source': tweet.source
                                                }, index=[i])], axis=0).drop_duplicates()
        i = i + 1

    tweets_df = tweets_df.drop(columns=tweets_df.columns.difference(['user_name', 'user_location', 'date', 'text', 'rating']))

    tweets_df = tweets_df.reset_index(drop=True)
    if ' ' in search_for:
        search_for = search_for.replace(" ", "")
    if not os.path.exists(unidecode(search_for).strip() + '_tweets.csv'):
        with open(unidecode(search_for).strip() + '_tweets.csv', "w") as my_empty_csv:
            my_empty_csv.close()
    tweets_df = pd.concat([tweets_df, pd.read_csv(unidecode(search_for).strip() + '_tweets.csv', index_col=0, header=0)], axis=0, ignore_index=True)
    len1 = len(tweets_df)
    tweets_df.drop_duplicates(subset=['user_name','text'], ignore_index=True, inplace=True)
    len2 = len(tweets_df)
    print(f'    New tweets fetched: {len1 - len2}       -       Total: {len2}')
    tweets_df.to_csv(unidecode(search_for).strip() + '_tweets.csv')

for item in search_for.split(','):
    get_tweets(item)