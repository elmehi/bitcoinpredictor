'''
some ideas:
1. only store items with more than 2 retweets (this should decrease the amount gather by 1/10 but request many more iterms and search for many more terms
2. search for fewer items
'''

from datetime import datetime, timedelta
# from pprint import pprint
import got3
from pymongo import MongoClient
import re

f = open('errorfile', 'w') 

queries = [
    'bitcoin%20',
    'bitcoin%20value%20OR%20price%20OR%20prices%20',
    'bitcoin%20blockchain%20OR%20miner%20OR%20dollar%20OR%20mining%20', 
    'bitcoin%20OR%20blockchain%20OR%20cryptocurrency%20',
    'bitcoin%20%20smart%20OR%20bank%20OR%20BTC%20'
    'bitcoin%20economy%20OR%20currency%20OR%20wallet%20',
    'mining%20"data%20center"%20OR%20algorithm%20',
    'etherium%20OR%20litecoin%20OR%20altcoin%20',
    'mt%20gox"%20OR%20Coindesk%20OR%20coinbase%20OR%20Pymnts%20OR%20CoinTelegraph%20OR%20Augur%20',
    ]

users = ['BitcoinMagazine', 'BitcoinPosts', 'BitcoinForums', 'Coinsecure', 'coin_fox','CryptorTrust'
'BitcoinEdu','bitcoinest','BitcoinOfficial']

'''  -------------------------------------------------------------------------------- '''
def getTweets(query, date, user):
    n = 40
    d_start = str(date)
    d_end = str(date + timedelta(1))
    description =  d_start + '\n'
    username = user
    print(description,)

    tweetCriteria = got3.manager.TweetCriteria().setSince(d_start).setUntil(d_end).setMaxTweets(n)
    if user != 0:  
        print('user:', username)
        tweetCriteria.setUsername(username)
    if query != 0: 
        print('query:', query)
        tweetCriteria.setQuerySearch(query)
    try:     
        tweet = got3.manager.TweetManager.getTweets(tweetCriteria)
        # tweetTo_d(tweet[0])
        return tweet
    except Exception as e:
        f.write(str(e) + '\n')

def modify(text):
    return re.split('http', text)[0]


def tweetTo_d(tweet):
    # assert len(tweet) == 1
    tweet_d = {}
    tweet_d['id'] = tweet.id
    tweet_d['permalink'] = tweet.permalink
    tweet_d['username'] = tweet.username
    tweet_d['text'] = modify(tweet.text)
    tweet_d['date'] = tweet.date 
    tweet_d['fromatted_date'] = tweet.formatted_date
    tweet_d['retweets'] = tweet.retweets
    tweet_d['favorites'] = tweet.favorites
    tweet_d['mentions'] = tweet.mentions
    tweet_d['hastags'] = tweet.hashtags
    tweet_d['geo'] = tweet.geo
    tweet_d['urls'] = tweet.urls
    tweet_d['user_id']  = tweet.author_id
    return tweet_d

def checkTwitter(date):
    client = MongoClient("mongodb://104.236.1.250:27017")
    db = client['local']
    for query in queries:
        results = getTweets(query, date, 0)
        if results == None: 
            f.write("no results" + '\n')
            continue
        for tweet in results:
            result = db.twitter.insert_one(tweetTo_d(tweet))
    for user in users:
        results = getTweets(0, date, user)
        if results == None: 
            f.write("no results" + '\n')
            continue
        for tweet in results:
            result = db.twitter.insert_one(tweetTo_d(tweet))
    return result

def processResults(search_date, endDate): 
    d_date_results = {}
    while search_date <= endDate:
        results = checkTwitter(search_date)
        d_date_results[search_date] = results
        search_date = search_date +  timedelta(1)

def main():
    now = datetime.utcnow().date()
    start_date = datetime(2015, 4, 16).date() 
    end_date = now
    processResults(start_date, end_date)

if __name__ == '__main__':
    main()