import requests
from threading import Thread


def crawl(url, results):
    data = requests.get(url).json()
    results += data['data']
    return True


def main(limit):
    print(limit)
    url = 'https://www.olx.ua/api/v1/offers/?offset={offset}&limit=50&category_id=65'
    urls = [url.format(offset=o) for o in range(0, limit, 50)]
    results = []
    threads = []

    for url in urls:
        process = Thread(target=crawl, args=[url, results])
        process.start()
        threads.append(process)

    for process in threads:
        process.join()

    return results
