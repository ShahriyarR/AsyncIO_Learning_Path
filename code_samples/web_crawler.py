import time
from urllib.request import urlopen


def get_urls_to_crawl():
    return [
        'http://www.cnn.com/',
        'https://www.foxnews.com/',
        'https://www.bbc.com/',
        'https://www.dawn.com',
        'https://www.cnbc.com',
        'https://www.twitter.com',
    ]


if __name__ == "__main__":

    urls_to_crawl = get_urls_to_crawl()
    start = time.time()

    for url in get_urls_to_crawl():
        html = urlopen(url)
        text = html.read()

    elapsed = time.time() - start
    print("\n{} URLS downloaded in {:.2f}s".format(len(urls_to_crawl), elapsed))