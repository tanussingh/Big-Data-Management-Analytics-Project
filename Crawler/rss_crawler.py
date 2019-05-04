"""
This script is used to collect articles on the sites that don't work with news-please out of the box.
"""

from newsplease import NewsPlease
from feedfinder2 import find_feeds
import feedparser
from pymongo import MongoClient
from datetime import datetime
import hjson
from tqdm import tqdm

# TODO: Use argparse to get command line arguments
db_name = "big_data"
collection_name = "spanish_articles"
client = MongoClient()
db = client[db_name]
articles = db[collection_name]

# these sites cause news-please to hang
blocked_sites = {
    'http://www.eluniversal.com.co/',
    'https://www.laopinion.com/'
}

if __name__ == "__main__":
    with open("config/sitelist_rss.hjson", "r") as s:
        sitelist = hjson.load(s)

    if 'base_urls' not in sitelist.keys():
        raise ValueError("HJSON file doesn't have sitelist key. Check News Please input format.")

    sitelist = sitelist['base_urls']

    for site in sitelist:
        if 'url' not in site:
            continue

        if site['url'] in blocked_sites:
            continue

        rss_links = find_feeds(site['url'])

        if len(rss_links) == 0:
            continue

        feed = feedparser.parse(rss_links[0])

        if 'entries' not in feed:
            continue

        print("Processing feed for", site['url'])

        for entry in tqdm(feed['entries']):
            if 'link' not in entry:
                continue

            try:
                article = NewsPlease.from_url(entry['link'])

                if articles.find_one({'url': article.url}) is None:
                    articles.insert_one({
                        'url': article.url,
                        'domain': article.source_domain,
                        'date_publish': article.date_publish,
                        'date_modify': article.date_modify,
                        'title': article.title,
                        'description': article.description,
                        'text': article.text,
                        'authors': article.authors
                    })
            except:
                continue
