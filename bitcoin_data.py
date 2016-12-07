import math
import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.model_selection import cross_val_score
from datetime import datetime as dt, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# from 

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

def getFitDirection(df):
    x = range(len(df['Date_Time']))
    y = df['Price']
    m, b = np.polyfit(x, y, 1)
    return m > 0

def sliceDf(start_date):
    df = pd.read_csv('data_new.csv', parse_dates=['Date','Date_Time'])
    # print(df)
    # start_date = start_date.date()
    start_index = df[df['Date'] == start_date].iloc[[0]].index.values[0]
    df = df[start_index:]
    df = df.set_index(['Date_Time'])
    # df.loc[:,'Date_Time'] = df.apply(convert_from_minutes, axis=1)
    # print(df)
    df = df[start_date:]
    # print(df)
    return(df)

def changePercent(df):
    pos = 0
    neg = 0
    p = df['Price']
    c = p.pct_change()
    for x in c:
        if x > 0: pos +=1 
        else: neg += 1
    tot = pos + neg
    print('perent pos:', pos/tot, 'percent neg:', neg/tot)

def grabTweets(twitter_start_date, retweets_min):
    db = MongoClient("mongodb://104.236.1.250:27017")['local']
    collection = db['twitter']
    print('regular grabbing tweets')
    tweets = list(collection.find({"date": {"$gt": twitter_start_date }, "retweets": {"$gte":retweets_min}}))
    return tweets

def grabTweetsStrategic(twitter_start_date, retweets_min):
    db = MongoClient("mongodb://104.236.1.250:27017")['local']
    collection = db['twitter']
    print('strategically grabbing tweets')
    content = list(collection.find({"date": {"$gt": twitter_start_date}, "retweets": {"$gte":retweets_min} }).sort("date", 1))
    revised_content = []
    new_text = ''
    date = content[0]['date']
    number_combined = 0
    for c in content:
        # pprint(c)
        if date.minute - c['date'].minute == 0:
            new_text = new_text + c['text'] + ' '
            # print(new_text)
            number_combined += 1
        else:
            # print('NUM COM:', number_combined, '\n', drop_seconds(date), '\n', new_text + '\n\n')
            revised_content.append({'date': drop_seconds(date), 'text': new_text})
            new_text = c['text'] + ' '
            number_combined = 0
            date = c['date']
    # pprint(revised_content)
    return revised_content

def classify(df, tweets, ma, mb, modeltype):
    targetdata = []
    
    content = [c['text'] for c in tweets]
    tfidf = TfidfVectorizer(input = 'content', stop_words=ENGLISH_STOP_WORDS)
    traindata = tfidf.fit_transform(content).toarray()
    
    for document in tweets:
        date = drop_seconds(document['date'])
        df_near_tweet = df[date - timedelta(minutes=mb):date + timedelta(minutes=ma)].reset_index()
        try: 
            targetdata.append(getFitDirection(df_near_tweet))
        except Exception as e:
            print("error:", e)
            print(df_near_tweet)

    # clf = modeltype().fit(traindata, targetdata)
    clf = modeltype()
    print("=====crossval:======")
    scores = cross_val_score(clf, traindata, targetdata, cv=3)                                             
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


def predictBitcoins(start_date, retweets_min, window_size, mt, minutes_before):
    #60% with 300 and 0
    #61% with 300, 150
    
    print('start date: ', start_date)
    print('minutes after: ', window_size) # '. minutes before:', MINUTES_BEFORE)
    print('minimum retweets: ', retweets_min)
    print('model type: ', str(mt))
    twitter_start_date = start_date + timedelta(days=1)
    df = sliceDf(start_date)
    changePercent(df)
    tweets = grabTweets(twitter_start_date, retweets_min)
    # tweets = grabTweetsStrategic(twitter_start_date)
    print('# of tweets', len(tweets))
    classify(df, tweets, window_size, minutes_before, mt)


def multiRun():
    minutes_before = 0
    SMs = [6, 7, 8, 9, 10]
    RMs = [0, 1, 5, 10]
    WSs = [200, 300, 400, 600]
    MTs = [MultinomialNB, LogisticRegression]
    for m in SMs:
        start_date = start_date = dt(2016, m, 1, 0, 0, 0)
        for retweets_min in RMs:
            for window_size in WSs:
                for mt in MTs:
                    return predictBitcoins(start_date, retweets_min, window_size, mt, minutes_before)

def singleRun():
    start_date = dt(2016, 8, 1, 0, 0, 0)
    window_size = 300
    minutes_before = 0
    retweets_min = 1
    mt = LogisticRegression
    return predictBitcoins(start_date, retweets_min, window_size, mt, minutes_before)

def main():
    multiRun()
    # singleRun()

    #consider adding in a few new features:
    # distance from time being searched, is there link?, how many hashtags?, sentiment analysis, retweets 

main()
