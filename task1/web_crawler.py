import time

import requests
from bs4 import BeautifulSoup


def generate_index_file():
    url = 'https://obrazovaka.ru/books'
    resp = requests.get(url)
    links = list()
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, features='html.parser')
        a_tags = soup.select('.short__item .item__bottom a')[:100]
        links = list(map(lambda a: a.get('href'), a_tags))
        with open('static/index.txt', mode='w') as file:
            for i, link in enumerate(links):
                file.write(f'{i+1} - {link}\n')
    else:
        print(f"Can't parse page {url}. Status code {resp.status_code}")
    return links


def download_page(url, path):
    resp = requests.get(url, stream=True)
    with open(path, mode='wb') as file:
        for chunk in resp.iter_content(chunk_size=128):
            file.write(chunk)


def main():
    links = generate_index_file()
    for i, link in enumerate(links):
        path = f'static/pages/{i+1}.html'
        try:
            download_page(link, path)
        except ConnectionError:
            time.sleep(10)
            download_page(link, path)
        if i % 5 == 0:
            print(f'Downloaded {i}/{len(links)}')
        time.sleep(15)


if __name__ == '__main__':
    main()
