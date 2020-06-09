import time
from urllib.request import urlopen
from multiprocessing import Process


def get_urls_to_crawl():
    return [
        'http://www.cnn.com/',
        'https://www.foxnews.com/',
        'https://www.bbc.com/',
        'https://www.dawn.com',
        'https://www.cnbc.com',
        'https://www.twitter.com',
    ]


def crawl_one_url(url_):
    html = urlopen(url_)
    text = html.read()


if __name__ == "__main__":

    urls_to_crawl = get_urls_to_crawl()
    start = time.time()

    processes = list()
    for url in get_urls_to_crawl():
        processes.append(Process(target=crawl_one_url, args=(url,)))

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    elapsed = time.time() - start
    print("\n{} URLS downloaded in {:.2f}s".format(len(urls_to_crawl), elapsed))