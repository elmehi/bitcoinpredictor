from pymongo import MongoClient
from pprint import pprint
from datetime import datetime as dt
db = MongoClient("mongodb://104.236.1.250:27017")['local']
collection = db['twitter']


# def get_subset():

def main():
    start_date = dt(2016, 10, 20)
    for document in collection.find({"date": {"$gt": start_date}}):
        d = document['date']
        d = dt(d.year, d.month, d.day, d.hour, d.minute)
        print(d)
main()
