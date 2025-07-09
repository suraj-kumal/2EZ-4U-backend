from bs4 import BeautifulSoup
import requests

from news.models import NewsAggregate,NewsSite

from django.conf import settings
from datetime import datetime 


def initialize(url,headers):
    articles = []
    try:
        res = requests.get(url,headers=headers)
        status_code = res.status_code
    except Exception as e:
        print("Error fetching url: {}".format(url))
    try:
        soup = BeautifulSoup(res.text,'xml')
        articles = soup.find_all('item')
    except Exception as e:
        print('Error parsing xml from url: {}'.format(url))
    return articles


def parse_nytimes_rss(news_site):
    url = 'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml'
    headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    articles = initialize(url,headers)
    data = []
    for article in articles:
        d = {}
        d['title'] = article.find('title').text
        d['link'] = article.find('atom:link')['href']
        d['description'] = article.find('description').text
        if(article.find('dc:creator')==None):
            d['creator']='na'
        else:
            d['creator'] = article.find('dc:creator').text
        d['pubdate'] = article.select('pubDate')[0].text
        if(article.find('media:content',{'medium':'image'})==None):
            d['media'] = 'na'
        else:
            d['media'] = article.find('media:content',{'medium':'image'})['url']
        if(article.find('media:description')==None):
            d['media_description']='na'
        else:
            d['media_description'] = article.find('media:description').text
        if(article.find('media:credit')==None):
            d['media_credit']='na'
        else:
            d['media_credit'] = article.find('media:credit').text
        categories = article.find_all('category')
        cat = []
        for c in categories:
            cat.append(c.text)
        cat = ','.join(cat)
        d['categories'] = cat
        data.append(d)
        ny = NewsAggregate(
            title=d['title'],
            link=d['link'],
            description=d['description'],
            creator = d['creator'],
            publication_date = d['pubdate'],
            media_url=d['media'],
            media_description=d['media_description'],
            media_credit = d['media_credit'],
            categories = d['categories'],
            news_site = news_site
            )
        ny.save()

def parse_foxnews_rss(news_site):
    url = 'http://feeds.foxnews.com/foxnews/scitech'
    headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }

    articles = initialize(url,headers)
    data = []
    for article in articles:
        d = {}
        d['title'] = article.find('title').text
        if(article.find('link')==None):
            d['link']='na'
        else:
            d['link'] = article.find('link').text
        d['description'] = article.find('description').text
        if(article.find('dc:creator')==None):
            d['creator']='na'
        else:
            d['creator'] = article.find('dc:creator').text
        if(article.find('pubDate')==None):
            d['pubdate']='na'
        else:
            d['pubdate'] = article.find('pubDate').text
        if(article.find('media:content',{'medium':'image'})==None):
            d['media'] = 'na'
        else:
            d['media'] = article.find('media:content',{'medium':'image'})['url']
        
        d['media_description']='na'
        d['media_credit']='na'
        d['categories']='na'
        data.append(d)
    # res = es.index(index="foxnews-index",body={'body':data,'timestamp':datetime.now()})
        fx = NewsAggregate(
            title=d['title'],
            link=d['link'],
            description=d['description'],
            creator = d['creator'],
            publication_date = d['pubdate'],
            media_url=d['media'],
            media_description=d['media_description'],
            media_credit = d['media_credit'],
            categories = d['categories'],
            news_site = news_site
            )
        fx.save()






# from celery import Celery
# from celery.schedules import crontab

# app = Celery()

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, parse_pcmag_rss.s('https://in.pcmag.com/feed.xml',headers), name='add every 10')

#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(60.0, parse_cnet_rss.s('https://www.cnet.com/rss/all/',headers), expires=10)

#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )

def parse_pcmag_rss(news_site):
    url = 'https://in.pcmag.com/feed.xml'
    headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }

    articles = initialize(url,headers)
    data = []
    for article in articles:
        d = {}
        d['title'] = article.find('title').text
        if(article.find('link')==None):
            d['link']='na'
        else:
            d['link'] = article.find('link').text
        d['description'] = article.find('description').text
        if(article.find('dc:creator')==None):
            d['creator']='na'
        else:
            d['creator'] = article.find('dc:creator').text
        if(article.find('pubDate')==None):
            d['pubdate']='na'
        else:
            d['pubdate'] = article.find('pubDate').text
        if(article.find('enclosure')==None):
            d['media'] = 'na'
        else:
            d['media'] = article.find('enclosure')['url']
        cat = []
        categories = article.find_all('category')
        for c in categories:
            cat.append(c.text)
        cat = ','.join(cat)
        d['categories'] = cat
        d['media_description']='na'
        d['media_credit']='na'
        data.append(d)
    # res = es.index(index="pcmag-index",body={'body':data,'timestamp':datetime.now()})
        pc = NewsAggregate(
            title=d['title'],
            link=d['link'],
            description=d['description'],
            creator = d['creator'],
            publication_date = d['pubdate'],
            media_url=d['media'],
            media_description=d['media_description'],
            media_credit = d['media_credit'],
            categories = d['categories'],
            news_site =news_site
            )
        pc.save()

def parse_engadget_rss(news_site):
    url = 'https://www.engadget.com/rss.xml'
    headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    articles = initialize(url,headers)
    data = []
    for article in articles:
        d = {}
        d['title'] = article.find('title').text
        if(article.find('link')==None):
            d['link']='na'
        else:
            d['link'] = article.find('link').text
        d['description'] = article.find('description').text
        if(article.find('dc:creator')==None):
            d['creator']='na'
        else:
            d['creator'] = article.find('dc:creator').text
        if(article.find('pubDate')==None):
            d['pubdate']='na'
        else:
            d['pubdate'] = article.find('pubDate').text
        if(article.find('media:content',{'medium':'image'})==None):
            d['media'] = 'na'
        else:
            d['media'] = article.find('media:content',{'medium':'image'})['url']
        
        d['media_description']='na'
        d['media_credit']='na'
        d['categories']='na'
        data.append(d)
        cnet = NewsAggregate(
            title=d['title'],
            link=d['link'],
            description=d['description'],
            creator = d['creator'],
            publication_date = d['pubdate'],
            media_url=d['media'],
            media_description=d['media_description'],
            media_credit = d['media_credit'],
            categories = d['categories'],
            news_site = news_site
            )
        cnet.save()


def parse_cnet_rss(news_site):
    url = 'https://www.cnet.com/rss/all/'
    headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    articles = initialize(url,headers)
    data = []
    for article in articles:
        d = {}
        d['title'] = article.find('title').text
        if(article.find('link')==None):
            d['link']='na'
        else:
            d['link'] = article.find('link').text
        d['description'] = article.find('description').text
        if(article.find('dc:creator')==None):
            d['creator']='na'
        else:
            d['creator'] = article.find('dc:creator').text
        if(article.find('pubDate')==None):
            d['pubdate']='na'
        else:
            d['pubdate'] = article.find('pubDate').text
        if(article.find('media:content',{'medium':'image'})==None):
            d['media'] = 'na'
        else:
            d['media'] = article.find('media:content',{'medium':'image'})['url']
        
        d['media_description']='na'
        d['media_credit']='na'
        d['categories']='na'
        data.append(d)
        cnet = NewsAggregate(
            title=d['title'],
            link=d['link'],
            description=d['description'],
            creator = d['creator'],
            publication_date = d['pubdate'],
            media_url=d['media'],
            media_description=d['media_description'],
            media_credit = d['media_credit'],
            categories = d['categories'],
            news_site = news_site
            )
        cnet.save()












