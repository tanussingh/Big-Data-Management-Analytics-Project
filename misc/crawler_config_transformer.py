# read a config file and generate a new file that uses RSSCrawler
import hjson
import json

config_file = "../Crawler/config/sitelist.hjson"
out_path = "../Crawler/config/sitelist_rss.hjson"

if __name__ == "__main__":
    with open(config_file, 'r') as f:
        data = hjson.load(f)
        base_urls = data['base_urls']

        url_list = [d['url'] for d in base_urls]
        final_base_urls = []
        for url in url_list:
            final_base_urls.append({
                'url': url,
                'crawler': 'RssCrawler'
            })

    with open(out_path, 'w') as o:
        json.dump({'base_urls': final_base_urls}, o)
