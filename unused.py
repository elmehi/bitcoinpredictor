import twitter
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

searchTerms = [
    'bitcoin%20',
    'bitcoin%20value%20OR%20price%20OR%20prices%20',
    'bitcoin%20blockchain%20OR%20miner%20OR%20dollar%20OR%20mining%20', 
    'bitcoin%20OR%20blockchain%20OR%20cryptocurrency%20',
    'bitcoin%20OR%20smart%20OR%20bank%20OR%20BTC%20',
    'bitcoin%20economy%20OR%20currency%20OR%20wallet%20',
    'mining%20"data%20center"%20OR%20algorithm%20',
    'etherium%20OR%20litecoin%20OR%20altcoin%20',
    'mt%20gox"%20OR%20Coindesk%20OR%20coinbase%20OR%20Pymnts%20OR%20CoinTelegraph%20OR%20Augur%20',
    'from%3ABitcoin%20OR%20from%3ABitcoinMagazine%20OR%20from%3ABitcoinPosts%20OR%20from%3ABitcoinForums%20',
    'from%3ACoinsecure%20OR%20from%3Ablockchain%20OR%20from%3Acoin_fox%20OR%20from%3ACryptorTrust%20',
    'from%3ABitcoinEdu%20OR%20from%3Abitcoinest%20OR%20from%3ABitcoinOfficial%20'
    ]


consumer_secret = 'SlYVsHsSlAEuS7tct2lyh9ng2n1WIAlBwEAVz2ImC82oetVMRH'
consumer_key = 'xmd9jJsNvaCaJJsMEIDGiyY9r'
access_token = '397739289-JNBN4QmrO72CuCG8HGDuaSVIpaeoTRBCxklBvUNc'
access_token_secret = 'AHhl3vyDWomtMVIj7TpgB6TqORMPJ74o8nHnpYq5wBqxq'

api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                   access_token_key=access_token, access_token_secret=access_token_secret, sleep_on_rate_limit=True)


def twitterScraper(query):
    url = u'https://twitter.com/search?q='+ query
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    tweets = [p.text for p in soup.findAll('p', class_='tweet-text')]
    for t in tweets:
        print(t)

def checkTwitter(date):
    # count = 30
    dstring = ''
    results = []

    # if date is not None:
    #     dstring = prepareDate(date)
    
    for t in searchTerms:
        query = t + dstring + '&src=typd&lang=en' # '&count=' + str(count)
        # print(query)
        # result = twitterScraper(query)
        # result = api.GetSearch(raw_query='q=' + query)
        results.append(result)
    return results

def test():
    x = api.GetSearch(raw_query='q=bit%20since%3A2016-1-5%20until%3A2016-1-6')
    pprint(x)
    print(len(x))

def prepareDate(date):
    dstart =  str(date.year) + '-' + str(date.month) + '-' + str(date.day) +'%20'
    date = date +  timedelta(1)
    dend =  str(date.year) + '-' + str(date.month) + '-' + str(date.day)
    dstring = 'since%3A' + dstart + 'until%3A' + dend #
    # print(dstring)
    return dstring

def parse_time(in_time):
    dt = datetime.strptime(in_time,'%a %b %d %H:%M:%S +0000 %Y')
    return dt

def printResults(o_results):
    for i, o in enumerate(o_results):
        print('\n')
        print(o['text'])


def results_O(results): 
    ids = set()   
    o_result = {}
    o_results = []
    c_duplicates = 0

    for result in results:
        for r in result:
            if r.id in ids:
                c_duplicates +=1
                continue

            created = parse_time(r.created_at)
            
            ids.add(r.id)
            o_result['id'] = r.id
            o_result['text'] = r.text
            o_result['timestamp'] = created
            o_result['author'] = r.user.screen_name
            o_result['url'] = r.urls
            o_result['media'] = r.media
            o_result['hashtags'] = r.hashtags
            o_results.append(dict(o_result))
            
    print(len(o_results))
    return o_results


def printTweet(descr, t):
        print(descr)
        print("Username: %s" % t.username)
        print("Retweets: %d" % t.retweets)
        print("Text: %s" % t.text)
        print("Mentions: %s" % t.mentions)
        print('Date', t.date)
        print("Hashtags: %s\n" % t.hashtags)
