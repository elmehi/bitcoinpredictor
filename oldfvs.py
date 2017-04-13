# from pymongo import MongoClient
# twitter_start_date = start_date + timedelta(days=1)

# db = MongoClient("mongodb://104.236.1.250:27017")['local']
# collection = db['twitter_two']
# print('regular grabbing tweets')
# tweets = list(collection.find({"date": {"$gt": twitter_start_date, "$lt": end_date}, "retweets": {"$gte":retweets_min}}))
# print('# of tweets grabbed:', len(tweets))
# print(tweets[1:10])

# def buildFVs(df, tweets, price_window, tweet_window, min_tweets, cutoff):
#     mFV = np.zeros(len(words_i_like))
#     date = tweets[0]['date']
#     last_date = df['Date'][-1] - timedelta(days=1)
#     tweet_count = 0
#     fvs = []
#     targetdata =[]
#     most_recent = []
#     counts = []
    
#     for tweet in tweets:
#         tFV = singleTweetFV(tweet['text'], tweet['retweets'])
#         if date.minute - tweet['date'].minute == 0:
#             mFV += tFV
#             tweet_count +=1
#         else:
#             if tweet_count > min_tweets:
#                 if date > last_date: break # return fvs, targetdata
#                 most_recent.append(mFV)
#                 if len(most_recent) > tweet_window:
#                     most_recent.pop(0) 
#                     fvs.append(sum(most_recent))
#                     targetdata.append(getDelta(df, np.datetime64(date), price_window, cutoff))
#                     counts.append(tweet_count)
#             mFV = np.zeros(len(words_i_like))
#             date = tweet['date']
#             tweet_count = 0
#     return fvs, targetdata

# fvs, target_data = buildFVs(df, tweets, price_window, tweet_window, min_tweets, cutoff)

# print('lenght of target data:', len(target_data))