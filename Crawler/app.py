from newsplease import NewsPlease

if __name__ == "__main__":
    article = NewsPlease.from_url('https://www.antena3.com', timeout=300)
    print(article.title)
