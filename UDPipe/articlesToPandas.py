import pandas as pd
import pymongo
from pymongo import MongoClient
from bson import ObjectId
import json, time
from datetime import datetime

# for encoding ObjectId as string
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def getDF():
    client = MongoClient("localhost", 27017)
    dbArticles = client['big_data']
    collection_Article= dbArticles['spanish_articles']

    articles = []
    if (collection_Article.count()) > 0:
        filter = {"date_publish": {"$gt": datetime(2019, 5, 5)}}
        for story in collection_Article.find(filter):
            articles.append(story)

    df = pd.DataFrame(articles, columns = ['_id', 'url', 'domain', 'date_modify', 'date_publish', 'title', 'description', 'text', 'authors'])
    print(df.head(25))

if __name__=="__main__": getDF()
