import pandas as pd
from pprint import pprint

base_config = {
    'base_urls': []
}

base_urls = []
all_urls = []


def convert_to_json(url):
    return {
        "url": url
    }


if __name__ == '__main__':
    data = '../spanish_sites.xlsx'

    sites_df = pd.read_excel(data)

    sites_list = sites_df['Links']

    all_urls = sites_list.tolist()
    cleaned_urls = [x for x in all_urls if type(x) == str]

    base_urls = [convert_to_json(url) for url in cleaned_urls]

    pprint(base_urls)
