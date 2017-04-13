x = ['+usb', 'usa', 'cointelegraph', 'action', 'lisk', 'hours', 'tonight', 'app', 'elite', 'coinigy', 'lottery', 'cap', 'investorseurope', 'ico', 'weekly', 'lawsuit', 'thrive', 'scam', 'service', 'economics', 'read', 'check', 'paper.li/cryptoelite/14', '26551318', 'usb3.0', 'west', 'ebook', 'drawing', '16x-1x', 'revolution', 'raise', 'industry', 'minimum', 'anoncoin', 'anc', '1000', '1hour', 'did', 'by…', 'low', 'profits', 'paper', 'strength', 'twitter', 'asic', 'markets', 'mybtccoin', 'claims', 'minutes', 'years', 'doge', 'internet', 'btcb0t', 'iot', 'bet', 'cex.io', 'days', 'rise', 'startups', 'wage', 'group', 'games', 'year', 'paypal', "'m", 'easiest', '347.86740437', 'hacked', 'website', 'rmb', 'payment', 'btcusd', 'eur||', 'wealth', 'services', 'utc', 'submitted', 'play', 'link', 'youtube.com/watch', 'antminer', 'banking', 'contracts', 'anonymous', '24', 'project', '/btc', '0.01', 'decentralized', 'litecoins', 'trust', 'usd/btc', 'let', 'del', 'community', 'used', 'ibm', 'tutorials', 'got', '2015s', 'wasted', 'address', 'forex', 'lumbridgecity', 'available', 'poloniex', 'case', 'soon', 'canada', 'mh', 'instant', 'look', 'que', 'learn', 'left', 'code', 'work', 'create', 'mark', 'w/', 'btctrade.web.fc2.com', 'webinars', 'x11', 'transactions', '500', 'goo.gl/iqfhcl', 'total', 'para', 'investing', 'better', 'sent', 'cryptsy', 'wallets', 'web', 'ready', 'earned', 'faucets', 'release', 'medium', 'trustee', 'bitmain', '..', '.5', 'ebay.to/1rb4upu', 'microsoft', 'source', 'media', 'mizuho', 'wow', 'government', 'transaction', 'uk', 'winkdex', 'btcnews', 'potcoin', 'center', 'try', 'judge', 'class', 'gbp', 'capital', 'changed', 'bring', 'brexit', 'sale', 'coming', 'cryptocurrencies', 'account', 'ccn', 'classic', 'worldcoinindex.com/coin/bitcoin', 'cny', 'itbit', 'stock', 'site', 'diversify', 'really', 'worth', 'conference', 'es', '23:35', 'announces', 'tinyurl.com/betmoose', 'moosepicks_', '19:17', 'profit', 'karpeles', 'ff3=2', 'vectorid=229466', 'england', 'lgeo=1', 'rover.ebay.com/rover/1/711-53', 'giveaway', '15', '200-19255-0/1', 'pot', 'talk', 'long', 'test', 'traffic', 'amid', 'claim', 'hit', 'mined', 'debit', 'following', 'based', 'hp', 'life', '0.05', 'fork', 'ebay.to/1msgbwg', 'bonus', 'offers', 'end', 'bankruptcy', 'playing', '2f', '700', 'privacy', '18', 'come', 'potbot', '2.0', 'supply', 'google', 'send', 'major', '600', 'plans', 'push', 'vs', 'usb', 'satoshis', 'satış', 'alış', 'blog', 'innovation', 'hard', 'bitlive', 'say', 'list', 'se', 'bitcointalk', 'looks', 'stories', 'fund', 'things', 'potential', 'biggest', 'firm', '2015', 'est', 'reveals', 'fiat', 'quote', 'zcash', 'public', 'making', 'eu', 'social', 'safe', 'store', 'fact', 'team', 'working', 'released', '50', 'magic', 'cada', 'contest', 'street', 'amp', '12', 'cryptochan', 'largest', 'bought', 'cur.lv/o99ed', 'medium.com/', 'investors', 'accepting', 'bit', 'accept', 'raises', 'sha', '19', 'stolen', 'prediction', 'company', 'uno', 'earning', 'rub', '.01', 'apple', 'satochis', 'increase', 'shiftがダウン', '-2016年のmt', 'traders', 'mybtccoin.com', 'toolid=10039', 'article', 'ビットコイン交換所shape', 'companies', "'re", 'developer', 'steemit', 'btcgbp', 'adds', 'btceur', 'となるか-', 'goo.gl/pnvbf2', 'e3', 'cards', 'man', 'private', 'gathering', 'run', 'venezuela', 'save', 'share', 'alerts', 'research']

def classify_old(df, tweets, ma, mb, modeltype):
    targetdata = []
    a, b = split_list([c['date'] for c in tweets])
    print('start_date', a[0], 'mid_date', b[0])
    content = [c['text'] for c in tweets]
    tfidf = TfidfVectorizer(input = 'content', stop_words=ENGLISH_STOP_WORDS)
    feature_vector = tfidf.fit_transform(content).toarray()
    # feature_vector = [[c['num'], 1] for c in tweets]
    
    for document in tweets:
        date = drop_seconds(document['date'])
        df_near_tweet = df[date - timedelta(minutes=mb):date + timedelta(minutes=ma)].reset_index()
        try: 
            targetdata.append(getFitDirection(df_near_tweet, 0.001))
        except Exception as e:
            print("error:", e)
            print(df_near_tweet)
    # standard_cross_val(modeltype, feature_vector, targetdata)        
    custom_cross_val(modeltype, feature_vector, targetdata) 


def standard_cross_val(modeltype, feature_vector, targetdata):
    clf = modeltype()
    print("=====crossval:======")
    scores = cross_val_score(clf, feature_vector, targetdata, cv=3)                                             
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
def grabTweetsStrategic(twitter_start_date, retweets_min):
    db = MongoClient("mongodb://104.236.1.250:27017")['local']
    collection = db['twitter_two']
    print('strategically grabbing tweets')
    content = list(collection.find({"date": {"$gt": twitter_start_date}, "retweets": {"$gte":retweets_min} }).sort("date", 1))
    revised_content = []
    new_text = ''
    date = content[0]['date']
    number_combined = 1
    for c in content:
        if date.minute - c['date'].minute == 0:
            new_text = new_text + c['text'] + ' '
            number_combined += 1
        else:
            p = 1 + TextBlob(new_text).sentiment.polarity
            revised_content.append({'date': drop_seconds(date), 'text': new_text, 'num': number_combined, 'pol': p})
            new_text = c['text'] + ' '
            number_combined = 1
            date = c['date']
    # pprint(revised_content)
    print('# of tweets grabbed:', len(revised_content))
    return revised_content
def studyWords(tweets):
    dwords = {}
    dphrases = {}
    for tweet in tweets:
        
        text = tweet['text'].lower()
        blob = TextBlob(text)
        # words = [x[0] for x in blob.tags]
        phrases = blob.noun_phrases
        
        # for word in words:
        #     if word not in dwords: dwords[word] = 1
        #     else: dwords[word] = dwords[word] + 1
        for phrase in phrases:
            if phrase not in dphrases: dphrases[phrase] = 1
            else: dphrases[phrase] = dphrases[phrase] + 1

    dwords = dphrases
    print(len(dwords))
    dwords = {k: dwords[k] for k in dwords if len(k) > 1 and k not in ENGLISH_STOP_WORDS}
    dwords = sorted(dwords.items(), key=lambda x: -1 * x[1])
    print([x[0] for x in dwords[:600]])
    print(dwords[599])

