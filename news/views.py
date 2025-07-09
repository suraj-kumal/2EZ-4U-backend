from django.shortcuts import render
from django.http import HttpResponse,Http404
from news.tasks import *
from news.models import NewsAggregate
from content.models import Subject
import random,json

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
def start_scrapper(request):
    news_sites = list( NewsSite.objects.all())
    for site in news_sites:
        if site.name =='NewYork Times':
            parse_nytimes_rss(site)
        elif site.name == 'Fox News':
            parse_foxnews_rss(site)
        elif site.name == 'PC Magazine':
            parse_pcmag_rss(site)
        elif site.name=='Engadget':
            parse_engadget_rss(site)
        else:
            parse_cnet_rss(site)
    return HttpResponse("Success")
        
def news_list(request):
    articles = []
    try:
        articles = list(NewsAggregate.objects.all().order_by('-created_at'))
    except NewsAggregate.DoesNotExist:
        raise Http404("Doesnot exists")
    random.shuffle(articles)
    subjects = Subject.objects.all()
    return render(request,'pages/news_list.html',{'articles':articles,'subjects':subjects})
def get_news(request,uid):
    article = None
    try:
        article = NewsAggregate.objects.get(uid=uid)
    except NewsAggregate.DoesNotExist:
        raise Http404("Doesnot exists")
    print(article.description)
    return render(request,'pages/news_page.html',{'article':article})

class TopFiveNews(APIView):
    def get(self, request):
        try:
            # Get all articles ordered by creation date and serialize them
            articles = list(NewsAggregate.objects.all().order_by('-created_at').values())
            random.shuffle(articles)  # Shuffle the list of articles
            top_five_articles = articles[:5]  # Get only the top five articles
            return Response(top_five_articles, status=status.HTTP_200_OK)
        except NewsAggregate.DoesNotExist:
            raise Http404("News articles do not exist")
    


