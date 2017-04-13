import requests
from bs4 import BeautifulSoup

url = u'https://twitter.com/search?q='
query = u'bitcoin%20'
r = requests.get(url+query)
soup = BeautifulSoup(r.text, 'html.parser')

tweets = [p.text for p in soup.findAll('p', class_='tweet-text')]
for t in tweets:
    print(t)