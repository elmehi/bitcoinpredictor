import twitter
from datetime import datetime, timedelta
# from pprint import pprint

consumer_secret = 'SlYVsHsSlAEuS7tct2lyh9ng2n1WIAlBwEAVz2ImC82oetVMRH'
consumer_key = 'xmd9jJsNvaCaJJsMEIDGiyY9r'
access_token = '397739289-JNBN4QmrO72CuCG8HGDuaSVIpaeoTRBCxklBvUNc'
access_token_secret = 'AHhl3vyDWomtMVIj7TpgB6TqORMPJ74o8nHnpYq5wBqxq'

api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                   access_token_key=access_token, access_token_secret=access_token_secret)

def parse_time(in_time):
    dt = datetime.strptime(in_time,'%a %b %d %H:%M:%S +0000 %Y')
    return dt

def prepareDate(date):
    dstart =  + date.year + '-' +date.month + '-' + date.day +'%20'
    date + 1
    dend =  + date.year + '-' +date.month + '-' + date.day +'%20'
    dstring = 'since%3A' + dstart + 'until%3A' + dend
    return dstring

def checkTwitter(date):
    dstring = ''
    if date is not None:
        dstring = prepareDate(date)
    searchTerms = [
    'q=bitcoin%20value%20OR%20price%20OR%20prices%20lang%3Aen&lang=en',
    'q=bitcoin%20blockchain%20OR%20miner%20OR%20dollar%20OR%20mining&lang=en', 
    'q=bitcoin%20OR%20blockchain%20OR%20cryptocurrency%20&lang=en',
    'q=bitcoin%20OR%20smart%20OR%20bank%20OR%20BTC%20&lang=en',
    'q=bitcoin%20economy%20OR%20currency%20OR%20wallet%20&lang=en',
    'q=bitcoin%20economy%20OR%20currency%20OR%20wallet%20&lang=en',
    'q=mining%20"data%20center"%20OR%20algorithm&lang=en',
    'q=etherium%20OR%20litecoin%20OR%20altcoin%20&lang=en',
    'q="mt%20gox"%20OR%20Coindesk%20OR%20coinbase%20OR%20Pymnts%20OR%20CoinTelegraph%20OR%20Augur&src=typd&lang=en',
    'q=from%3ABitcoin%20OR%20from%3ABitcoinMagazine%20OR%20from%3ABitcoinPosts%20OR%20from%3ABitcoinForums',
    'q=from%3ACoinsecure%20OR%20from%3Ablockchain%20OR%20from%3Acoin_fox%20OR%20from%3ACryptorTrust',
    'q=from%3ABitcoinEdu%20OR%20from%3Abitcoinest%20OR%20from%3ABitcoinOfficial'
    ]
    results = []

    for t in searchTerms:
        results.append(api.GetSearch(raw_query= t + dstring))
    
    return results

results = checkTwitter(datetime.date(2002, 3, 11))

array_results = []
sum_results = 0
res_ds = []
res_d = {}
ids = set()
counter_tooOld = 0
counter_duplicates = 0

oldest = datetime.utcnow() 
newest = datetime(1990, 1, 1)

for result in results:
    for s in result:
        if s.id in ids:
            counter_tooOld += 1
            continue

        created = parse_time(s.created_at)
        
        ids.add(s.id)
        res_d['id'] = s.id
        res_d['text'] = s.text
        res_d['timestamp'] = created
        res_d['author'] = s.user.screen_name
        res_d['url'] = s.urls
        res_d['media'] = s.media
        res_d['hashtags'] = s.hashtags
        # print(s.text)
        if (datetime.utcnow()-created < timedelta(minutes=10)): 
            res_ds.append(dict(res_d))

            if created < oldest: oldest = created
            if created > newest: newest = created
        else: counter_duplicates +=1
        
    sum_results = len(result) + sum_results
    array_results.append(len(result))

for i, o in enumerate(res_ds):
    print('\n')
    print(o['text'])
    # pprint(o)

print('\n\n', sum_results, " results ", array_results)
print("useful results:", len(res_ds))
print('removed duplicates: ', counter_duplicates)
print('removed for time: ', counter_tooOld)
print(newest - oldest)