# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, request, jsonify, make_response, render_template, flash, redirect, url_for, session, escape, g
#from flask.ext.login import login_required
from collections import defaultdict

import requests
from xml.etree import ElementTree
import pprint
from datetime import datetime
import json
import ruter
import xkcd
import lunch

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

front = Blueprint('front', __name__, template_folder='front')

# Add CSS sheet only for unauthenticated urls
@front.context_processor
def css_processor():
    return dict(css_file='/static/css/front.css')

def index():
    return render_template('front/index.html')

def plain():
    return render_template('front/plain.html')

def about():
    return render_template('front/about.html')


def get_sun():
    sun = cache.get('day_oslo')
    if not sun:
        get_yr()
        sun = cache.get('day_oslo')

    dayrise = datetime.strptime(sun['rise'], '%Y-%m-%dT%H:%M:%S')
    dayset = datetime.strptime(sun['set'], '%Y-%m-%dT%H:%M:%S')
    return "Sun up %s and sun down %s" % (str(dayrise.time()), str(dayset.time()))
    #return sun

def get_yr():
    url = 'http://www.yr.no/place/Norway/Oslo/Oslo/Oslo/varsel_time_for_time.xml'
    #url = 'http://localhost/varsel_time_for_time.xml'
    #print tree
    data = cache.get('weather_data_oslo')
    day = cache.get('day_oslo')

    if not data:
        r = requests.get(url)
        tree = ElementTree.fromstring(r.content)
        print "Getting the data"
        data = defaultdict(dict)
        day = None

        for child in tree:
            if child.tag == 'sun':
                day = child.attrib
            for elem in child:
                if elem.tag == 'tabular':
                    for item in elem:
                        data[item.attrib['from']]['time'] = item.attrib
                        # This is a time unit
                        for i in item:
                            # This is the content of time
                            data[item.attrib['from']][i.tag] = i.attrib

        cache.set('weather_data_oslo', data, timeout=60*30)
        cache.set('day_oslo', day, timeout=60*60*12)

    return day, data

def yr():
    url = 'http://www.yr.no/place/Norway/Oslo/Oslo/Oslo/varsel_time_for_time.xml'
    #url = 'http://localhost/varsel_time_for_time.xml'
    day, data = get_yr()
    dayrise = datetime.strptime(day['rise'], '%Y-%m-%dT%H:%M:%S')
    dayset = datetime.strptime(day['set'], '%Y-%m-%dT%H:%M:%S')
    print "Sun up %s and sun down %s" % (str(dayrise.time()), str(dayset.time()))

    link = "http://symbol.yr.no/grafikk/sym/b38/%s.png"

    newdata = []
    #pprint.pprint(dict(data))
    #print len(data)
    for key, value in data.iteritems():
        n = []
        n.append(key)
        n.append(value['temperature']['value'])
        n.append(link % value['symbol']['var'])
        newdata.append(n)

    # http://symbol.yr.no/grafikk/sym/b38/09.png
    # http://symbol.yr.no/grafikk/sym/b38/mf/40n.73.png

    # TODO: SORT ARRAY
    #print sorted(newdata)[0:12]

    return str(json.dumps(sorted(newdata)[0:12]))

def get_ruter():
    stop = ruter.find_stops('holbergs plass')
    print stop
    if stop:
        req = requests.get(ruter.base + 'RealTime/GetAllDepartures/' + str(stop))
        departures = req.json()

    out = []
    if departures:
        for line in departures:
            out.append(ruter.print_stop(line))

    return str(json.dumps(out[0:10]))

def get_weather_now():
    day, data = get_yr()
    link = "http://symbol.yr.no/grafikk/sym/b100/%s.png"
    newdata = []
    for key, value in data.iteritems():
        n = []
        n.append(key)
        n.append(value['temperature']['value'])
        n.append(link % value['symbol']['var'])
        newdata.append(n)

    n = sorted(newdata)[0]
    return str(json.dumps(n))

def get_toppsaker():
    #r = requests.get("http://www.nrk.no/toppsaker.rss")
    r = requests.get("http://www.nrk.no/nyheter/siste.rss")
    #a = ""
    #for chunk in r.iter_content(20):
        #a += chunk
    resp = make_response(r.content)
    resp.mimetype = 'text/plain'
    return resp

def get_xkcd(random=None):
    if random:
        title, alt, img = xkcd.get_xkcd(random=True)
    else:
        title, alt, img = xkcd.get_xkcd(random=False)
    print title, alt, img
    return json.dumps({"title": title, "alt": alt, "img": img})

def get_lunch():
    #url = cache.get('lunch')
    #if url is None:
        ##url = lunch.get_lunch()
        #url = lunch.get_random()
        #cache.set('lunch', url, timeout=12*60*60) #12 hours
    url = lunch.get_lunch()
    return json.dumps({"img": url, "title": "Lunch"})

# URLs
front.add_url_rule('/about/', 'about', about)
front.add_url_rule('/', 'index', index)
front.add_url_rule('/plain', 'plain', plain)
front.add_url_rule('/yr', 'yr', yr)
front.add_url_rule('/get_ruter', 'get_ruter', get_ruter)
front.add_url_rule('/get_sun', 'get_sun', get_sun)
front.add_url_rule('/get_weather_now', 'get_weather_now', get_weather_now)
front.add_url_rule('/get_toppsaker', 'get_toppsaker', get_toppsaker)
front.add_url_rule('/get_xkcd/', 'get_xkcd', get_xkcd)
front.add_url_rule('/get_xkcd/<random>', 'get_xkcd', get_xkcd)
front.add_url_rule('/get_lunch', 'get_lunch', get_lunch)
