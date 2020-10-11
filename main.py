#!/usr/bin/python3

import os

from bs4 import BeautifulSoup
import requests


MAIN_URL = 'https://opensource.apple.com/tarballs/'
DOWNLOAD_DIR = 'appleopensource'


def download(url, local_filename):
    print(local_filename)
    response = requests.get(url)
    received = 0
    assert response.status_code == 200

    with open(local_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                received += 1024
                f.write(chunk)


def get_all_categories():
    soup = BeautifulSoup(requests.get(MAIN_URL).text, 'html.parser')
    retval = set()

    # first 3 are the table headers
    for tr in soup.select('.column tr')[3:]:
        tr = str(tr)
        if 'href' not in tr:
            continue

        retval.add(tr.split('href="', 1)[1].split('"', 1)[0])

    return retval


def main():
    for category in get_all_categories():
        soup = BeautifulSoup(requests.get(MAIN_URL + category).text, 'html.parser')

        # first 3 are the table headers
        for tr in soup.select('.column tr')[3:]:
            tr = str(tr)
            if 'href' not in tr:
                continue

            filename = tr.split('href="', 1)[1].split('"', 1)[0]

            if '-' not in filename:
                # skip unversion filenames
                continue

            dirname = os.path.join(DOWNLOAD_DIR, category)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            local_filename = os.path.join(dirname, filename)
            remote_file_data = MAIN_URL + category + filename
            download(remote_file_data, local_filename)


if __name__ == '__main__':
    main()
