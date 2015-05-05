Thesis dashboard
================
Based on the repo Flask-Bootstrap (flask bootstrap basis template)

This provides a basic informational screen with information from the following
providers:

 - NRK Breaking news (RSS newsfeed)
 - Ruter (Norwegian public transport firm for Oslo) real time (Based on
   https://github.com/larhauga/RuterShell)
 - Yr (Norwegian meteorological institution)
 - XKCD and Lunch comic caching && inline placement

## NOTICE
This product is not intended for further use.
Used as a informational screen during the writing of my master thesis, and
written in a hurry :)

Beware of a lot of dirty awefull inline css!!!! Yes, I hate myself too.
Time-to-market, blabla.

## Run
Easiest you can do is the following:

```
docker build -t web .
docker run -d -P web
```
