#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import random
import requests
from BeautifulSoup import BeautifulSoup
from datetime import datetime


def get_lunch(site=None):
    if not site or 'tu' in site:
        r = requests.get('http://www.tu.no/lunch/')
        soup = BeautifulSoup(r.content)
        imgurl = soup.findAll("div", {"class": "image"})[0].img['src']
    elif site in 'dagbladet':
        r = requests.get('http://www.dagbladet.no/tegneserie/lunch/')
        soup = BeautifulSoup(r.content)
        imgurl = soup.find(id='lunch-stripe')['src']

    return imgurl

def get_image(url, storepath):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(storepath, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def get_random():
    sites = ['tu', 'dagbladet']
    return get_lunch(site=sites[random.randint(0,1)])

def main():
    #get_lunch()
    #title, alt, img = get_lunch()
    folder = '/home/lars/striper'
    if not os.path.exists(folder):
        os.makedirs(folder)

    sites = ['tu', 'dagbladet']
    #sites = ['dagbladet']
    for site in sites:
        if not os.path.exists(os.path.join(folder, site)):
            os.makedirs(os.path.join(folder, site))
        img = get_lunch(site=site)
        if img:
            path = os.path.join(folder, site, img.split('/')[-1])
            if 'dagbladet' in site:
                path = os.path.join(folder, site, datetime.now().isoformat())
                path += ".png"

            if not os.path.exists(path):
                get_image(img, path)
        else:
            print "Could not find image: %s" % img

if __name__ == '__main__':
    main()
