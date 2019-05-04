# the crawler has to be run manually in multi-site mode. 
# this part is responsible for digging into data directory 
# and putting articles into mongo

from pymongo import MongoClient
from tqdm import tqdm
from os import walk
from os.path import exists, join
from datetime import datetime
import pickle
import json
import os.path
import argparse

parser = argparse.ArgumentParser(description="""Reads the news articles crawled by news-please and adds them to
the mongo""")
parser.add_argument('--data', type=str, help='Data directory where articles are stored')
parser.add_argument('--db', type=str, default='big_data', help='Name of mongo database')
parser.add_argument('--collection', type=str, default='spanish_articles',
                    help='Name of collection to store articles in')
args = parser.parse_args()

already_crawled_file = '/Users/ishan/Work/GitHub/BD_Project/data/py/indexed.pkl'


def save_already_crawled_list():
    with open(already_crawled_file, 'wb') as save_file:
        pickle.dump(already_crawled, save_file)


if os.path.exists(already_crawled_file):
    with open(already_crawled_file, 'rb') as f:
        already_crawled = pickle.load(f)
else:
    already_crawled = set()


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
    file_set = set()
    if exists(data_dir):
        for dir_path, directories, files in walk(data_dir):
            # ignoring the temporary path created by crawler
            if '.resume_jobdir' in dir_path:
                continue

            # if there are files present, we want to read only if format is JSON
            if len(files) > 0:
                for filename in files:
                    if '.json' in filename:
                        file_set.add(join(dir_path, filename))
                # print("Processing", dir_path)

        to_crawl = file_set - already_crawled
        crawled = 0

        for filepath in tqdm(to_crawl):
            with open(filepath, 'r') as f:
                data = json.load(f)
                if data['text'] is not None and data['language'] == 'es':
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
                already_crawled.add(filepath)
                crawled += 1
                # save after we have processed 100 files
                if crawled % 100:
                    save_already_crawled_list()
    else:
        raise ValueError("Data directory does not exist.")

save_already_crawled_list()
