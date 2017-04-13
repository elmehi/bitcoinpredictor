import math
import pandas as pd
import numpy as np
from collections import defaultdict
# from textblob import TextBlob
from pymongo import MongoClient
# from sklearn.model_selection import cross_val_score
from datetime import datetime as dt, timedelta
# from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
# from sklearn.tree import DecisionTreeClassifier
# from sklearn import tree
# import time
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# from pprint import pprint

words_i_like = ['bitcoin', 'btc', 'blockchain', 'litecoin', 'usd',
'wallet', 'currency', 'altcoin', 'mining', 'gox', 'mt', 'crypto', 'new', 
'cryptocurrency', 'ethereum', 'fintech', 'ltc', 'free', 'digital', 'latest',
'money', 'bank', 'hardware', 'index', 'satoshi', 'market', 'economy', 'bitcoins',
'dogecoin', 'value', 'secure', 'miner', 'trading', 'coindesk', 'smart', 
'bitstamp', 'technology', 'euro', 'buy', 'trade', 
'coinbase', 'power', 'time', 'tech', 'trezor', 'bitfinex', 'algorithm', 'china', 'banks', 
'earn', 'past', 'landbitcoin', 'portal', 'win',
 'data', 'coin', 'best', 'cash', 'bitcoinnews', 'increased', 'cloud', 'average', 
'future', 'change', 'financial', 'virtual', 'startup', 'open', 'ceo', 'platform', 
'decreased', 'business', 'finance', 'convert', 'high', 'dash', 'altcoins', 'currencies', 
'collapse', 'libertarian', 'bot', 'dollar', 'movement', 'directly', 'game',
'global', 'technical', 'investment', 'launches', 'volume', 'network', 'support',
'observer', 'lost', 'security', 'secure', 'won', 'good', 'launch', 
'gambling', 'japan', 'invest', 'sell', 'wild', 'hack', 
'pay', 'exchanges', 'miners', 'crypto-currencies', 'forum', 'fast', 'sell', 'ledger', 
'mobile', 'grow', 'hot', 'great', 'wild', 'hack', 'miracle', 'bullish', 'solution', 'millionare']

def split_list(a_list):
    half = int(len(a_list)/2)
    return a_list[:half], a_list[half:]

def convert_from_minutes(x):
    d = x[1]
    m = x[2]
    h = math.floor(m/60)
    m = int(m % 60)
    d = d.replace(hour=h, minute=m)
    return d

def drop_seconds(d):
    d = dt(d.year, d.month, d.day, d.hour, d.minute)
    return d

# def getFitDirection(df, cutoff):
#     x = range(len(df['Date_Time']))
#     y = df['Price']
#     m, b = np.polyfit(x, y, 1)
#     if m > 0: return 2
#     # if m < cutoff and m > -cutoff: return 1
#     if m < 0: return 0
#     return 1

def sliceDf(start_date):
    df = pd.read_csv('data_new.csv', parse_dates=['Date','Date_Time'])
    start_index = df[df['Date'] == start_date].iloc[[0]].index.values[0]
    df = df[start_index:]
    df = df.set_index(['Date_Time'])
    df = df[start_date:]
    return(df)

# def df_PositiveLinePercent(df, tweet_window):
#     pos = 0
#     x = int(len(df['Date'])/50)
#     dlist = df['Date'].sample(x)
#     for d in dlist:
#         df_near_tweet = df[d:d + timedelta(minutes=tweet_window)].reset_index()
#         if getFitDirection(df_near_tweet, 0) > 1: pos +=1
#     return len(dlist), pos/len(dlist)

def getNearest(t, df):
    i = df.index.searchsorted(t)
    return df.iloc[i]['Price']

def getDelta(df, date, delta_minutes, cutoff):
    date = np.datetime64(date)
    df2 = df[:-(2*delta_minutes)]
    t1 = date
    t2 = date + np.timedelta64(delta_minutes,'m')
    p1 = getNearest(t1, df)
    p2 = getNeareste(t2, df2)
    m = p2-p1
    if m > cutoff: return 2
    if m < -cutoff: return 0
    return 1 

def df_DeltaPercent(df, tweet_window):
    df2 = df[:-(5*tweet_window)]
    pos = 0
    x = int(len(df['Date'])/200)
    dlist = np.random.choice(df2.index.values, x)
    for d in dlist:
        delta = getDelta(df, d, tweet_window, 0)
        if delta == -1: x-=1
        if delta > 1: pos +=1
    return x, pos/x

def showsomething(df, tweets, tweet_window):
    df2 = df[:-(5*tweet_window)]
    tweet_prices = []
    non_tweet_prices = []

    y = int(len(df['Date'])/100)
    tlist = np.random.choice(tweets, y)
    for document in tlist:
        date = drop_seconds(document['date'])
        tweet_prices.append(getDelta(df, date, tweet_window, 0))

    x = int(len(df['Date'])/200)
    dlist = np.random.choice(df2.index.values, x)
    for d in dlist:
        delta = getDelta(df, d, tweet_window, 0)
        non_tweet_prices.append(delta)
    print('number of_non_tweets sampled:', )
    
    return len(non_tweet_prices), sum(tweet_prices)/len(tweets)/2, sum(non_tweet_prices)/len(x)/2

def grabTweets(twitter_start_date, end_date, retweets_min):
    db = MongoClient("mongodb://104.236.1.250:27017")['local']
    collection = db['twitter_two']
    print('regular grabbing tweets')
    tweets = list(collection.find({"date": {"$gt": twitter_start_date, "$lt": end_date}, "retweets": {"$gte":retweets_min}}))
    print('# of tweets grabbed:', len(tweets))
    # print(tweets)
    return tweets

def buildFVs(df, tweets, price_window, tweet_window, min_tweets, cutoff):
    print('buildFVs')
    minute_data = np.zeros(len(words_i_like))
    date = tweets[0]['date']
    last_date = df['Date'][-1] - timedelta(days=1)
    tweet_count = 0
    fvs = []
    targetdata =[]
    most_recent = []

    for tweet in tweets:
        counts = defaultdict(int)
        for word in tweet['text'].lower().split(' '):
            word = word.lstrip('#')
            counts[word] = counts[word] + 1
        fv = np.zeros(len(words_i_like))
        for i, word in enumerate(words_i_like): fv[i] = counts[word]
        fv *= (tweet['retweets'] + 1)
        if date.minute - tweet['date'].minute == 0:
            minute_data += fv
            tweet_count +=1
        else:
            # print(minute_data, np.linalg.norm(minute_data))
            if tweet_count > min_tweets:
                if date > last_date: return fvs, targetdata
                # if np.linalg.norm(minute_data) != 0:
                #     most_recent.append(minute_data / np.linalg.norm(minute_data))
                # else:
                most_recent.append(minute_data)
                if len(most_recent) > tweet_window:
                    most_recent.pop(0)
                    window_fvs = sum(most_recent)
                    date = np.datetime64(date)
                    targetdata.append(getDelta(df, date, price_window, cutoff))
                    fvs.append(window_fvs)
            minute_data = np.zeros(len(words_i_like))
            date = tweet['date']
            tweet_count = 0
    return fvs, targetdata

def customVal(modeltype, feature_vector, target_data):
    print('MODEL: ', modeltype)
    guessedup = 0
    fva, fvb = split_list(feature_vector)
    tda, tdb = split_list(target_data)
    clf = modeltype.fit(fva, tda)
    pred = clf.predict(fvb)
    # prob = clf.predict_proba(fvb)
    
    print("percentage of predictions up:", pred.mean()/2)
    print("percentage of target up:", sum(tdb)/len(tdb)/2)
    count = total = 0
    for i, x in enumerate(pred):
        if x != 1 and tdb[i] != 1:
            count += 1
            if x == 2: guessedup+=1
            if x == tdb[i]: total += 1
    print('(amount removed:', (len(pred) - count)/len(pred), '%)')
    print('percent_accurate:', total/count)

    return clf

def predict(start_date, end_date, price_window, tweet_window, min_tweets, retweets_min, cutoff):
    print('======== Tuning ========')
    print('start date: ', start_date)
    print('price – minutes after tweet: ', price_window) # '. minutes before:', MINUTES_BEFORE)
    print('tweet window: ', tweet_window)
    print('minimum tweets in window: ', min_tweets)
    print('minimum retweets: ', retweets_min)
    print('cutoff:', cutoff)
    print('========================')
    df = sliceDf(start_date) 
    tweets = grabTweets(start_date + timedelta(days=1), end_date, 0)
    # number_samples, nonTweet_percentPos, tweet_percentPos = showsomething(df, tweets, tweet_window)
    number_samples, nonTweet_percentPos = df_DeltaPercent(df, price_window)
    print('For', number_samples, 'instances of', price_window, 'minute periods, The percent pos is:', nonTweet_percentPos)   
    # print('For tweets, the percent percent pos is:', tweet_percentPos)
    fvs, target_data = buildFVs(df, tweets, price_window, tweet_window, min_tweets, cutoff)
    print('lenght of target data:', len(target_data))
    # print(fvs[1::100])
    # print(target_data[1::100])
    for mt in [MultinomialNB(), LogisticRegression(), RandomForestClassifier(n_estimators=5000)]:
        customVal(mt, fvs, target_data) 
    # clf = customVal(DecisionTreeClassifier(), fvs, target_data)
    # tree.export_graphviz(clf, out_file='tree.dot', feature_names=words_i_like) 

# def multiRun():
#     minutes_before = 0
#     SMs = [6, 7, 8, 9, 10]
#     RMs = [0, 1, 5, 10]
#     WSs = [200, 300, 400, 600]
#     MTs = [MultinomialNB, LogisticRegression]
#     for m in SMs:
#         start_date = start_date = dt(2016, m, 1, 0, 0, 0)
#         for retweets_min in RMs:
#             for tweet_window in WSs:
#                 for mt in MTs:
#                     predictBitcoins(start_date, retweets_min, tweet_window, mt, minutes_before)

def singleRun():
    # MTs = [MultinomialNB, LogisticRegression, RandomForestClassifier]
    start_date = dt(2016, 4, 1, 0, 0, 0)
    end_date = dt(2016, 11, 23, 0, 00, 00)
    price_window = 200
    tweet_window = 200
    min_tweets = 2
    retweets_min = 0
    cutoff = .25
    # mt = MTs[2]
    return predict(start_date, end_date, price_window, tweet_window, min_tweets, retweets_min, cutoff)

def main():
    # multiRun()
    singleRun()
    #consider adding in a few new features:
    # distance from time being searched, is there link?, how many hashtags?, sentiment analysis, retweets 

main()
