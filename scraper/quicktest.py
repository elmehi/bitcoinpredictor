from datetime import datetime as dt, timedelta
start_date = dt(2016, 1, 1, 0, 0, 0) #best results when train from 4/2016 and onward # maybe do small window retraining
end_date = dt(2016, 11, 23, 0, 0, 0)
price_window = 200
tweet_window = 200
min_tweets = 1
cutoff = .25
retweets_min = 0

# set up db
from pymongo import MongoClient

db = MongoClient("mongodb://104.236.1.250:27017")['bitcoin_scraped']
db.authenticate('meir', 'PreemPalver', source='bitcoin_scraped')
collection = db['scraped1agg']
count_min = 0
retweet_min = 0
t1 = len(list(collection.find({"_id": {"$lt": end_date}, "count": {"$gte": count_min},"retweets_total": {"$gte": retweet_min}}, { '_id':1}).sort([("_id", 1)])))
t2 = len(list(collection.find({"count": {"$gte": count_min},"retweets_total": {"$gte": retweet_min}}, { '_id':1}).sort([("_id", 1)])))
t3 = len(list(collection.find({"count": {"$gte": count_min}}, { '_id':1}).sort([("_id", 1)])))
print(t1, t2, t3)