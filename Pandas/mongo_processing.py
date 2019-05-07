"""
Read articles from a collection, use a trained model to convert them to vectors and calculate similarity scores
for each document against document for that day
"""

from gensim.models import Doc2Vec
from pymongo import MongoClient
from datetime import datetime, timedelta
from Pandas.dov2vec import calculate_similarity
from misc.doc2vec import EpochLogger  # needed to load the model
from misc.text_processing import process_df as clean_text
import json
import pandas as pd

db_name = "big_data"
read_collection_name = "spanish_articles"
write_collection_name = "d2v_calculated"
d2v_model = Doc2Vec.load("../misc/models/doc2vec_2019.model")

start_date = datetime(2019, 4, 29, 0, 0, 0)
end_date = datetime(2019, 5, 7, 0, 0, 0)

current_start = start_date

if __name__ == "__main__":
    client = MongoClient()
    db = client[db_name]
    r_collection = db[read_collection_name]
    w_collection = db[write_collection_name]

    while current_start < end_date:
        # get all articles for current day
        current_end = current_start + timedelta(days=1)

        # build mongo query for articles for today
        query = {
            "$and": [
                {"date_publish": {"$gt": current_start}},
                {"date_publish": {"$lt": current_end}}
            ]
        }

        # get documents
        docs = [article for article in r_collection.find(query)]

        # convert to dataframe
        docs_df = pd.DataFrame(docs, columns=[
            '_id',
            'url',
            'domain',
            'date_modify',
            'date_publish',
            'title',
            'description',
            'text',
            'authors'
        ])

        # limit data for testing
        # docs_df = docs_df.head(100)

        # clean text
        docs_df = clean_text(docs_df)

        # drop the _id column created by Mongo
        docs_df = docs_df.drop(['_id'], axis=1)

        # calculate similarity
        similarity_df = calculate_similarity(docs_df, model=d2v_model, verbose=True)

        # write back to mongo collection
        to_insert = []
        for article in similarity_df.itertuples():
            to_insert.append({
                'url': article.url,
                'domain': article.domain,
                'date_publish': article.date_publish,
                'title': article.title,
                'd2v_sim': json.dumps(article.d2v_sim),  # converting to JSON required to avoid mongo error
                'd2v_dup_count': article.d2v_dup_count
            })

        print(len(to_insert), "articles processed for",
              current_start.strftime("%Y-%m-%d"), "-", current_end.strftime("%Y-%m-%d"))

        w_collection.insert_many(to_insert)
        current_start = current_end
