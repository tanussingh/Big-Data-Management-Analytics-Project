# the crawler has to be run manually in multi-site mode. 
# this part is responsible for digging into data directory 
# and putting articles into mongo

from pymongo import MongoClient
from tqdm import tqdm
from os import walk
from os.path import exists, join
from datetime import datetime
import json
import argparse

parser = argparse.ArgumentParser(description="""Reads the news articles crawled by news-please and adds them to
the mongo""")
parser.add_argument('--data', type=str, help='Data directory where articles are stored')
parser.add_argument('--db', type=str, default='big_data', help='Name of mongo database')
parser.add_argument('--collection', type=str, default='spanish_articles',
                    help='Name of collection to store articles in')
args = parser.parse_args()

if __name__ == '__main__':
    data_dir = args.data
    db_name = args.db
    collection_name = args.collection

    client = MongoClient()
    db = client[db_name]
    articles = db[collection_name]

    # data directory will have multiple directories
    # we need to go in till we get only files and then
    # read json files and put them in db
    if exists(data_dir):
        for dir_path, directories, files in walk(data_dir):
            # ignoring the temporary path created by crawler
            if '.resume_jobdir' in dir_path:
                continue

            # if there are files present, read only if format is JSON
            if len(files) > 0:
                print("Processing", dir_path)

            for filename in tqdm(files):
                if '.json' in filename:
                    filepath = join(dir_path, filename)
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        if data['text'] is not None:
                            if articles.find_one({'url': data['url']}) is None:
                                articles.insert_one({
                                    'url': data['url'],
                                    'domain': data['source_domain'],
                                    'date_modify': datetime.strptime(data['date_modify'], '%Y-%m-%d %H:%M:%S'),
                                    'date_publish': datetime.strptime(data['date_publish'], '%Y-%m-%d %H:%M:%S'),
                                    'title': data['title'],
                                    'description': data['description'],
                                    'text': data['text'],
                                    'authors': data['authors']
                                })
    else:
        raise ValueError("Data directory does not exist.")
