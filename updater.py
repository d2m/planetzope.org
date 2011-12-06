# -*- coding: utf-8 -*-

import base64
import datetime
import hashlib
import json
import os
import pickle
import re
import rfc822
import time
import urllib
import urllib2

import templates

def path(name):
    return os.path.join(os.getcwd(), name)

# folder to store downloaded feeds
data = path('data')
# feed urls to aggregate
feeds = path('urls.txt')
# index to downloaded feeds
feedlookup = []
# number of days to display in result listing
collect_num_days = 30
# filter words to be found in title, description or subject
filter = ['zope', 'zope2', 'zope3', 'ztk', 'zodb', 'bluebream', 'planetzope']
# feed content is always included
always_found = ['http://zope.org/news.rss',]
# feed content is always included if pattern matches feed url substring (for batched query urls)
always_search = ['http://plone.org/documentation/howto/search_rss',]
# feeds always ignored
always_ignore = ['http://blog.d2m.at/feed',]
# month names shortcuts
month = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
# files written by the script
feedlookupdata = path('feedlookup.txt')
planetfile = path('planet.pickle')
webpagefile = path('planet.html')
planetzopefile = path('index.html')
rssfeedfile = path('feed_rss.xml')
aggregatorfile = path('aggregator.txt')

class Entry:
    pass

class Planet:
    entries = []

def get_sha1(url):
    """create hash from url
    """
    sha1 = hashlib.sha1()
    sha1.update(url)
    urlsha1 = sha1.hexdigest()
    return urlsha1

def get_feedurls():
    """read feed urls from config file
    ignore lines with leading hash"""
    return [x.strip() for x in open(feeds).readlines() if x[0] != '#']

def get_feeddata():
    """read feed data from stored files
    """
    return [(os.path.join(data,get_sha1(url)), url) for url in get_feedurls()]

def update_feeds():
    """read all feedcontents from google and store it to a folder
    """
    feedurls = get_feedurls()
    for url in feedurls:
        query_args = { 'q': url, 'v':'1.0', 'num': '30' }
        qs = urllib.urlencode(query_args)
        loader = 'http://ajax.googleapis.com/ajax/services/feed/load'
        loadurl = '%s?%s' % (loader, qs)
        request = urllib2.Request(loadurl)
        request.add_header('Referer', 'http://www.planetzope.org/aggregator.txt')
        response = urllib2.urlopen(request)
        feed = response.read()
        urlsha1 = get_sha1(url)
        feedlookup.append((urlsha1, url))        
        feeddata = open(os.path.join(data, urlsha1),'wb')
        feeddata.write(feed)
        feeddata.close()
        print urlsha1, url
        time.sleep(1)
    fld = open(feedlookupdata, 'w')
    for a, b in feedlookup:
        fld.write('%s\t%s\n' % (a, b))
    fld.close()
    print 'feeds done'

def update_planet():
    """create pickled, filtered feed db from json files
    """
    datenow = time.time()
    all_feeds = {}
    for datei, url in get_feeddata():
        try:
            daten = json.loads(open(datei).read())
            feed = daten['responseData']['feed']
            if feed['entries'] == []:
                print 'no entries:', feed['feedUrl']
                continue
        except:
            print 'error:', url, datei
            continue
        all_feeds[feed['link']] = feed['title']
        for entry in feed['entries']:
            if entry['link'] in always_ignore:
                continue
            search = '%s %s %s' % (entry['title'], entry['content'], ', '.join(entry['categories']))
            search = search.lower()
            search = search.replace('<', ' ')
            search = search.replace('>', ' ')
            found = 0
            dateok = 0
            if feed['feedUrl'] in always_found:
                found = 1
            for i in always_search:
                if feed['feedUrl'].find(i)>-1:
                    found = 1
                    break
            for i in filter:
                if search.find(i) > -1:
                    found = 1
                    print 'match: %s', entry['link']
                    break
            if found:
                rfcdate = rfc822.parsedate(entry['publishedDate'])
                if rfcdate:
                    date = time.mktime(rfcdate) - 7*3600
                    pydate = date + collect_num_days*3600*24
                    if pydate >= datenow:
                        dateok = 1
                else:
                    print 'no date:', feed['feedUrl']
            if dateok:
                print 'entry:', entry['link'], date
                e = Entry()
                e.feedurl = feed['feedUrl']
                e.feedtitle = feed['title']
                e.feedlink = feed['link']
                e.title = entry['title']
                e.link = entry['link']
                e.content = entry['content']
                e.categories = entry['categories']
                e.publishedDate = entry['publishedDate']
                e.pubDate = '%s-%02d' % (month[time.localtime(date)[1]], time.localtime(date)[2])
                e.date = date
                e.pubDatedate = '%s %s' % (e.date, e.pubDate)
                planetzope.entries.append(e)
    planetzope.allfeeds = all_feeds
    pf = open(planetfile, 'wb')
    pickle.dump(planetzope, pf)
    pf.close()
    print 'db done'

def update_webpage():
    """create result listing to be included into html file
    """
    pf = open(planetfile)
    data = pickle.load(pf)
    pf.close()
    entries = reversed(sorted([(x.pubDatedate, x) for x in data.entries]))
    date_heading = ''
    out = []
    counter = 0
    today = time.time()
    for x, entry in entries:
        print entry.pubDatedate, entry.title.encode('utf-8', 'ignore')
        date = entry.date
        since = int((today - date) / (3600.0*24.0))
        sincetxt = ''
        if since == 0:
            sincetxt = 'today'
        elif since == 1:
            sincetxt = 'yesterday'
        else:
            sincetxt = '%s days ago' % since
        entry.since = sincetxt
        if entry.content:
            entry.counter = counter
            counter += 1
            template = templates.entry_content % entry.__dict__
        else:
            template = templates.entry_nocontent % entry.__dict__
        out.append(template)
    wp = open(webpagefile, 'w')
    wp.write(''.join(out).encode('utf-8','ignore'))
    wp.close()
    print 'planet done'
            
def update_planetzope_960():
    template = templates.html
    dt=datetime.datetime.utcnow()
    time_now = dt.strftime("%a, %d %b %Y %H:%M GMT")
    pf = open(planetfile)
    data = pickle.load(pf)
    pf.close()
    all_feeds = data.allfeeds
    keywords = str(list(sorted(filter)))
    out=[]
    for k, v in all_feeds.items():
        x = v.lower()
        y = ''
        for c in x:
            if c.isalnum() or c.isspace():
                y += c
        out.append((y.strip(), v, k))
    out.sort()
    blogroll = ['<div id="blogroll">']
    for x, k, v in out:
        blogroll.append('- <a href="%s">%s</a><br />' % (v.encode('utf-8', 'ignore'), k.encode('utf-8', 'ignore')))
    blogroll.append('</div>')
    blogroll = templates.blogroll % keywords
    for x, k, v in out:
        blogroll +=  '%40s ... %s\n' % (k[:40], v)
    af = open(aggregatorfile, 'w')
    af.write(blogroll.encode('utf-8', 'ignore'))
    af.close()
    pf = open(webpagefile).read()
    pzp = template % (time_now, pf, keywords)
    pzf = open(planetzopefile, 'w')
    pzf.write(pzp)
    pzf.close()
    print 'index done'

def update_rssfeed():
    pf = open(planetfile)
    data = pickle.load(pf)
    pf.close()
    entries = list(reversed(sorted([(x.pubDatedate, x) for x in data.entries])))[:15]
    resources = []
    for key, entry in entries:
        resources.append(entry.link)
    rdf_li_resources = '\n'.join(['<rdf:li resource="%s" />' % x for x in resources]) 
    template_item = templates.rdf_item
    template_subject = '<dc:subject>%s</dc:subject>'
    template_date = '<dc:date>%s</dc:date>'
    template_items=[]
    for key, entry in entries:
        subjects = ''
        if entry.categories:
            subjects = '\n'.join([template_subject % x for x in entry.categories])
        entry.subjects = subjects
        date = rfc822.parsedate(entry.publishedDate)
        entry.dcdate = template_date % time.strftime("%Y-%m-%dT%H:%M:%S-07:00", date)
        template_items.append(template_item % entry.__dict__)
    items_rdf_about = '\n'.join(template_items)
    
    template = templates.rdf % (rdf_li_resources, items_rdf_about)
    rff = open(rssfeedfile, 'w')
    rff.write(template.encode('utf-8', 'ignore'))
    rff.close()
    print 'rss done'


def main():
    update_feeds()
    update_planet()
    update_webpage()
    update_planetzope_960()
    update_rssfeed()
    
planetzope = Planet()

if __name__ == '__main__':
    main()
    
