import twitter
from datetime import datetime, timedelta
from pprint import pprint

consumer_secret = 'SlYVsHsSlAEuS7tct2lyh9ng2n1WIAlBwEAVz2ImC82oetVMRH'
consumer_key = 'xmd9jJsNvaCaJJsMEIDGiyY9r'
access_token = '397739289-JNBN4QmrO72CuCG8HGDuaSVIpaeoTRBCxklBvUNc'
access_token_secret = 'AHhl3vyDWomtMVIj7TpgB6TqORMPJ74o8nHnpYq5wBqxq'

api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                   access_token_key=access_token, access_token_secret=access_token_secret)


''' 
--------------------------------------------------------------------------------
'''

def parse_time(in_time):
    dt = datetime.strptime(in_time,'%a %b %d %H:%M:%S +0000 %Y')
    return dt

def prepareDate(date):
    dstart =  str(date.year) + '-' + str(date.month) + '-' + str(date.day) +'%20'
    # date = date +  timedelta(1)
    dend =  str(date.year) + '-' + str(date.month) + '-' + str(date.day)
    dstring = 'since%3A' + dstart + 'until%3A' + dend #
    print(dstring)
    return dstring

def test():
    x = api.GetSearch(raw_query='q=etherium%20OR%20litecoin%20OR%20altcoin%20since%3A2016-1-1%20until%3A2016-1-2%20&lang%3Aen&count%3A20')
    pprint(x)
    print(len(x))

def checkTwitter(date):
    count = 30
    dstring = ''

    if date is not None:
        dstring = prepareDate(date)

    # dstring = ''
    searchTerms = [
    'q=bitcoin%20value%20OR%20price%20OR%20prices%20',
    'q=bitcoin%20blockchain%20OR%20miner%20OR%20dollar%20OR%20mining%20', 
    'q=bitcoin%20OR%20blockchain%20OR%20cryptocurrency%20',
    'q=bitcoin%20OR%20smart%20OR%20bank%20OR%20BTC%20',
    'q=bitcoin%20economy%20OR%20currency%20OR%20wallet%20',
    'q=mining%20"data%20center"%20OR%20algorithm%20',
    'q=etherium%20OR%20litecoin%20OR%20altcoin%20',
    'q="mt%20gox"%20OR%20Coindesk%20OR%20coinbase%20OR%20Pymnts%20OR%20CoinTelegraph%20OR%20Augur%20',
    'q=from%3ABitcoin%20OR%20from%3ABitcoinMagazine%20OR%20from%3ABitcoinPosts%20OR%20from%3ABitcoinForums%20',
    'q=from%3ACoinsecure%20OR%20from%3Ablockchain%20OR%20from%3Acoin_fox%20OR%20from%3ACryptorTrust%20',
    'q=from%3ABitcoinEdu%20OR%20from%3Abitcoinest%20OR%20from%3ABitcoinOfficial%20'
    ]

    results = []

    for t in searchTerms:
        query = t + '&lang%3Aen%20' + dstring + '&count=' + str(count)
        
        # print(query)
        results.append(api.GetSearch(raw_query=query))
        # print(results)
    return results

def resultsToDict(results): 
    ids = set()   
    result_objects = []
    result_object = {}
    # counter_tooOld = 0
    counter_duplicates = 0
    array_results = []
    sum_results = 0

    for result in results:
        for s in result:
            if s.id in ids:
                counter_duplicates +=1
                continue

            created = parse_time(s.created_at)
            
            ids.add(s.id)
            result_object['id'] = s.id
            result_object['text'] = s.text
            result_object['timestamp'] = created
            result_object['author'] = s.user.screen_name
            result_object['url'] = s.urls
            result_object['media'] = s.media
            result_object['hashtags'] = s.hashtags
            result_objects.append(dict(result_object))
            # print(s.text)
            # if (datetime.utcnow()-created < timedelta(minutes=10)): 
            #     result_objects.append(dict(result_object))

            #     if created < oldest: oldest = created
            #     if created > newest: newest = created
            
            
        sum_results = len(result) + sum_results
        array_results.append(len(result))

    
    print('\n\n', sum_results, " results ", array_results)
    print("useful results:", len(result_objects))
    print('removed duplicates: ', counter_duplicates)
    # print('removed for time: ', counter_tooOld)
    # print(newest - oldest)

    return array_results

def processResults():
    now = datetime.utcnow() 
    results_by_date = {}
    search_date = datetime(2016, 11, 15)

    while search_date is not now:
        results = checkTwitter(search_date)
        storedResults = resultsToDict(results)

        results_by_date[search_date] = storedResults

        search_date = search_date +  timedelta(1)

    for k in results_by_date.keys():
        print((k, results_by_date[k]))

def printResults(result_objects):
    for i, o in enumerate(result_objects):
        print('\n')
        print(o['text'])
        # pprint(o)


processResults()