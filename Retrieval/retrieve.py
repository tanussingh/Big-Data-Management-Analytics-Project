import pymongo
from pymongo import MongoClient
import datetime
import json

def main():

    start = datetime.datetime.strptime('2019-04-01', '%Y-%m-%d')
    end = datetime.datetime.strptime('2019-04-01', '%Y-%m-%d')

    # Set up connection to Mongo Server
    client = MongoClient("localhost", 27017)

    # Set connection to database
    collection_Article = client[articles]

    # For ever file in every directory perform streaming
    for doc in articles.file.find({'created_at': {'$gt': start, '$lt': end}}):
        #Do whatever needs to be done

if __name__ == "__main__"
    main()
