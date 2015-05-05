#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import requests
from BeautifulSoup import BeautifulSoup


def get_xkcd(random=False):
    if random:
        r = requests.get('http://c.xkcd.com/random/comic/')
    else:
        r = requests.get('http://xkcd.com')
    soup = BeautifulSoup(r.content)
    imgurl = soup.find(id="comic").img['src']
    title = soup.find(id="comic").img['title']
    alt = soup.find(id="comic").img['alt']

    return title, alt, imgurl

def get_image(url, storepath):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(storepath, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def main():
    title, alt, img = get_xkcd()
    get_image(img, '/home/lars/code/xkcd/' + img.split('/')[-1])

if __name__ == '__main__':
    main()
