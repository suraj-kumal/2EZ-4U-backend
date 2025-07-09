
from django.shortcuts import render
from content.models import Subject,Chapter,Topic,Material,Notice,YouTube,CourseType,SeoContent,EngineeringProject,EngineeringProjectCategory
from blog.models import Article
from news.models import NewsAggregate,NewsSite
from django.http import Http404,JsonResponse,HttpResponse
from django.db.models import Prefetch
from content.serializers import *
import requests
import json
import random
from bs4 import BeautifulSoup

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated,AllowAny


# Create your views here.
def get_ads_txt(request):
    line="google.com, pub-2413501485945953, DIRECT, f08c47fec0942fa0"
    return HttpResponse(line)


def handleSearch(request):
    search_query = request.GET.get('search_query', '')
    subjects = Subject.objects.filter(title__icontains=search_query)
    serializer = SubjectSerializer(subjects,many=True)
    return JsonResponse(serializer.data)

def aboutus(request):
    content = "The contents are designed by Infography technologies Pvt Ltd. We aim at providing free online courses and tutorial in computer engineering domain."
    subjects = Subject.objects.filter(is_active=True)
    # context_dict = {'subjects':subjects}
    return render(request,'pages/aboutus.html',{'content':content,'subjects':subjects})

def get_notice(request):
    try:
        notices = Notice.objects.all().order_by('created_at')
    except Notice.DoesNotExist:
        raise Http404("Doesnot exists")
    subjects = Subject.objects.filter(is_active=True)
    return render(request,'pages/notice.html',{'notices':notices,'subjects':subjects})
def subject_list(request):
    subjects = Subject.objects.filter(is_active=True)
    context_dict = {'subjects':subjects}
    return render(request,'pages/course.html',context=context_dict)  


def index(request):
    try:
        course_type = CourseType.objects.filter(slug='course-material')[0]
        # course_type = CourseType.objects.all()[0]
    except CourseType.DoesNotExist:
        raise Http404("Doesnot exists")
    try:
        news_sites = NewsSite.objects.all()
    except NewsSite.DoesNotExist:
        raise Http404("Doesnot exists")
    articles = []
    for site in news_sites:
        article_list = list(NewsAggregate.objects.filter(news_site = site).order_by('-created_at'))
        if (len(article_list)>=3):
            articles.extend(article_list[:3])
    subjects = Subject.objects.filter(is_active=True,course_type=course_type)
    you_tube = YouTube.objects.order_by('-created_at')[:3]
    blogs = Article.objects.all().order_by('-created_at')[:3]
    random.shuffle(articles)
    context_dict = {'subjects':subjects,'videos':you_tube,'blogs':blogs,'articles':articles}
    return render(request,'pages/index.html',context=context_dict)

def course_detail(request,slug):
    try:
        subject = Subject.objects.get(is_active=True,slug=slug)
    except Subject.DoesNotExist:
        raise Http404("Course Doesnot exists")

    try:
        chapter_qs = Chapter.objects.filter(subject=subject).order_by('order_priority')
        chapter_qs = chapter_qs.prefetch_related(Prefetch('topic_set',queryset=Topic.objects.filter(is_active=True),to_attr='related_topics'))
    except Chapter.DoesNotExist:
        raise Http404("Chapter and Topics doesnot exists")
    chapter_topic = {}
    for chapter in chapter_qs:
        chapter_topic[chapter] = []
        for topic in chapter.related_topics:
            chapter_topic[chapter].append(topic)
    initial_topic = None
    for chapter in chapter_qs:
        for topic in chapter.related_topics:
            initial_topic = topic
            break
        break
    try:
        initial_content = Material.objects.get(topic__slug=initial_topic.slug)
        subjects = Subject.objects.filter(is_active=True)
    except Exception as e:
        print(e)
        return render(request,'pages/pagenotfound.html')
    
    try:
        materials = list(Material.objects.all())
        prev_content = 0
        next_content = materials[1].topic.slug 
    except Exception as e:
        return render(request,'pages/pagenotfound.html')
    
    try:
        seo = SeoContent.objects.get(subject=subject)
    except SeoContent.DoesNotExist:
        pass

    return render(request,'pages/course_content.html',context={'chapters_and_topics':chapter_topic,'initial_content':initial_content,'subject':subject,'subjects':subjects,'prev':prev_content,'next':next_content,'seo':seo,topic:topic})

def content_detail(request,slug):
    try:
        content = Material.objects.get(topic__slug=slug)
    except Material.DoesNotExist:
        data = {'content':'<h1>content not found</h1>'}
        return JsonResponse(data,safe=False)
    serializer = MaterialSerializer(content)
    return JsonResponse(serializer.data)

def content_detail_by_slug(request,slug):
    try:
        content = Material.objects.get(topic__slug=slug)
    except Material.DoesNotExist:
        data = {'content':'<h1>content not found</h1>'}
        return JsonResponse(data,safe=False)
    try:
        topic_cur = Topic.objects.get(uid = content.topic.uid)
    except Topic.DoesNotExist:
        data = {'content':'<h1>content not found</h1>'}
        return JsonResponse(data,safe=False)
    try:
        chapter_cur = Chapter.objects.get(uid = topic_cur.chapter.uid)
    except Topic.DoesNotExist:
        data = {'content':'<h1>content not found</h1>'}
        return JsonResponse(data,safe=False)
    try:
        subject = Subject.objects.get(uid = chapter_cur.subject.uid)
    except Subject.DoesNotExist:
        data = {'content':'<h1>content not found</h1>'}
        return JsonResponse(data,safe=False)
    
    # try:
    #     subject = Subject.objects.get(is_active=True,slug=slug)
    # except Subject.DoesNotExist:
    #     raise Http404("Course Doesnot exists")
    try:
        chapter_qs = Chapter.objects.filter(subject=subject).order_by('order_priority')
        chapter_qs = chapter_qs.prefetch_related(Prefetch('topic_set',queryset=Topic.objects.filter(is_active=True),to_attr='related_topics'))
    except Chapter.DoesNotExist:
        raise Http404("Chapter and Topics doesnot exists")
    chapter_topic = {}
    for chapter in chapter_qs:
        chapter_topic[chapter] = []
        for topic in chapter.related_topics:
            chapter_topic[chapter].append(topic)
    initial_topic = None
    for chapter in chapter_qs:
        for topic in chapter.related_topics:
            initial_topic = topic
            break
        break
    try:
        initial_content = Material.objects.get(topic__slug=initial_topic.slug)
        subjects = Subject.objects.filter(is_active=True)
    except Exception as e:
        print(e)
        return render(request,'pages/pagenotfound.html')
    try:
        current_topics = chapter_topic[chapter_cur]
        current_index = current_topics.index(topic_cur)
        if current_index==0:
            prev_content = 0
            if(len(current_topics)>1):
                next_content = current_topics[1].slug
            else:
                next_content = 0
        elif current_index == len(current_topics)-1:
            next_content = 0
            if(len(current_topics)>1):
                prev_content = current_topics[-2].slug
            else:
                prev_content = 0
        else:
            prev_content = current_topics[current_index-1].slug
            next_content = current_topics[current_index+1].slug
    except Exception as e:
        print(e)
        return render(request,'pages/pagenotfound.html')

    try:
        seo = SeoContent.objects.get(subject=subject)
    except SeoContent.DoesNotExist:
        pass
    return render(request,'pages/course_content_single.html',context={'chapters_and_topics':chapter_topic,'initial_content':initial_content,'subject':subject,'subjects':subjects,'content':content.content,'pdf_file':content.pdf_file,'prev':prev_content,'next':next_content,'seo':seo,'topic':topic})

# for tutorial
def tutorial_home(request):
    try:
        course_type = CourseType.objects.filter(slug='tutorial')[0]
        # course_type = CourseType.objects.all()[0]
    except CourseType.DoesNotExist:
        raise Http404("Doesnot exists")

    subjects = Subject.objects.filter(is_active=True,course_type=course_type)
    context_dict = {'subjects':subjects}
    return render(request,'pages/tutorial.html',context=context_dict)

def tutorial_detail(request,slug):
    try:
        subject = Subject.objects.get(is_active=True,slug=slug)
    except Subject.DoesNotExist:
        raise Http404("Course Doesnot exists")

    try:
        chapter_qs = Chapter.objects.filter(subject=subject).order_by('order_priority')
        chapter_qs = chapter_qs.prefetch_related(Prefetch('topic_set',queryset=Topic.objects.filter(is_active=True),to_attr='related_topics'))
    except Chapter.DoesNotExist:
        raise Http404("Chapter and Topics doesnot exists")
    chapter_topic = {}
    for chapter in chapter_qs:
        chapter_topic[chapter] = []
        for topic in chapter.related_topics:
            chapter_topic[chapter].append(topic)
    initial_topic = None
    for chapter in chapter_qs:
        for topic in chapter.related_topics:
            initial_topic = topic
            break
        break
    try:
        initial_content = Material.objects.get(topic__slug=initial_topic.slug)
        subjects = Subject.objects.filter(is_active=True)
    except Exception as e:
        print(e)
        return render(request,'pages/pagenotfound.html')
    
    try:
        materials = list(Material.objects.all())
        prev_content = 0
        next_content = materials[1].topic.slug 
    except Exception as e:
        return render(request,'pages/pagenotfound.html')
    
    try:
        seo = SeoContent.objects.get(subject=subject)
    except SeoContent.DoesNotExist:
        pass

    return render(request,'pages/tutorial_content.html',context={'chapters_and_topics':chapter_topic,'initial_content':initial_content,'subject':subject,'subjects':subjects,'prev':prev_content,'next':next_content,'seo':seo,topic:topic})

def tutorial_detail_by_slug(request,slug):
    print('hii')
    try:
        content = Material.objects.get(topic__slug=slug)
    except Material.DoesNotExist:
        data = {'content':'<h1>content not found</h1>'}
        return JsonResponse(data,safe=False)
    try:
        topic_cur = Topic.objects.get(uid = content.topic.uid)
    except Topic.DoesNotExist:
        data = {'content':'<h1>content not found</h1>'}
        return JsonResponse(data,safe=False)
    try:
        chapter_cur = Chapter.objects.get(uid = topic_cur.chapter.uid)
    except Topic.DoesNotExist:
        data = {'content':'<h1>content not found</h1>'}
        return JsonResponse(data,safe=False)
    try:
        subject = Subject.objects.get(uid = chapter_cur.subject.uid)
    except Subject.DoesNotExist:
        data = {'content':'<h1>content not found</h1>'}
        return JsonResponse(data,safe=False)
    
    # try:
    #     subject = Subject.objects.get(is_active=True,slug=slug)
    # except Subject.DoesNotExist:
    #     raise Http404("Course Doesnot exists")
    try:
        chapter_qs = Chapter.objects.filter(subject=subject).order_by('order_priority')
        chapter_qs = chapter_qs.prefetch_related(Prefetch('topic_set',queryset=Topic.objects.filter(is_active=True),to_attr='related_topics'))
    except Chapter.DoesNotExist:
        raise Http404("Chapter and Topics doesnot exists")
    chapter_topic = {}
    for chapter in chapter_qs:
        chapter_topic[chapter] = []
        for topic in chapter.related_topics:
            chapter_topic[chapter].append(topic)
    initial_topic = None
    for chapter in chapter_qs:
        for topic in chapter.related_topics:
            initial_topic = topic
            break
        break
    try:
        initial_content = Material.objects.get(topic__slug=initial_topic.slug)
        subjects = Subject.objects.filter(is_active=True)
    except Exception as e:
        print(e)
        return render(request,'pages/pagenotfound.html')
    try:
        current_topics = chapter_topic[chapter_cur]
        current_index = current_topics.index(topic_cur)
        if current_index==0:
            prev_content = 0
            if(len(current_topics)>1):
                next_content = current_topics[1].slug
            else:
                next_content = 0
        elif current_index == len(current_topics)-1:
            next_content = 0
            if(len(current_topics)>1):
                prev_content = current_topics[-2].slug
            else:
                prev_content = 0
        else:
            prev_content = current_topics[current_index-1].slug
            next_content = current_topics[current_index+1].slug
    except Exception as e:
        print(e)
        return render(request,'pages/pagenotfound.html')

    try:
        seo = SeoContent.objects.get(subject=subject)
    except SeoContent.DoesNotExist:
        pass
    return render(request,'pages/tutorial_content_single.html',context={'chapters_and_topics':chapter_topic,'initial_content':initial_content,'subject':subject,'subjects':subjects,'content':content.content,'pdf_file':content.pdf_file,'prev':prev_content,'next':next_content,'seo':seo,'topic':topic})


def engineering_project_home(request):
    categories = EngineeringProjectCategory.objects.filter(is_active=True)
    projects = EngineeringProject.objects.filter(is_active=True)
    return render(request,'pages/ep.html',context={'categories':categories,'projects':projects})

def engineering_project_detail(request,slug):
    categories = EngineeringProjectCategory.objects.filter(is_active=True)
    projects = EngineeringProject.objects.filter(project_category__slug=slug,is_active=True)
    return render(request,'pages/ep_detail.html',context={'categories':categories,'projects':projects})


# APIs defined here 

from rest_framework.permissions import BasePermission

class TokenAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.auth is not None
    

class CourseTypeList(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request):
        items = CourseType.objects.filter(is_active=True)
        serializer = CourseTypeSerializer(items,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class CourseTypeDetail(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request,slug):
        items = CourseType.objects.filter(is_active=True,slug=slug)
        serializer = CourseTypeSerializer(items,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class SubjectList(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request):
        subjects = Subject.objects.filter(is_active=True)
        serializer = SubjectSerializer(subjects,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class SubjectDetail(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request,slug):
        subjects = Subject.objects.filter(is_active=True,slug=slug)
        serializer = SubjectSerializer(subjects,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    

class TopicListBySubject(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request,subject_slug):
        subject = Subject.objects.get(slug=subject_slug)
        chapters = Chapter.objects.filter(subject=subject).order_by('order_priority')
        serializers = ChapterDetailSerializer(chapters,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

    
class MaterialByTopic(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request,topic_slug):
        topic = Topic.objects.get(slug=topic_slug)
        material = Material.objects.get(topic=topic)
        serializer = MaterialSerializer(material)
        return Response(serializer.data,status=status.HTTP_200_OK)  



class YouTubeList(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request):
        youtube = YouTube.objects.order_by('-created_at')[:3]
        serializer = YoutubeSerializer(youtube,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class SeoDetail(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request,course_slug):
        subject = Subject.objects.get(slug=course_slug)
        seo = SeoContent.objects.get(subject=subject)
        serializer = SeoContentSerializer(seo)
        return Response(serializer.data,status=status.HTTP_200_OK)     


class ChapterList(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request):
        chapters = Chapter.objects.filter(is_active=True)
        serializer = ChapterSerializer(chapters,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ChapterDetail(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request,slug):
        chapters = Chapter.objects.filter(is_active=True,slug=slug)
        serializer = ChapterSerializer(chapters,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class TopicList(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request):
        topics = Topic.objects.filter(is_active=True)
        serializer = TopicSerializer(topics,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class TopicDetail(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request,slug):
        topics = Topic.objects.filter(is_active=True,slug=slug)
        serializer = TopicSerializer(topics,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class MaterialList(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request):
        materials = Material.objects.filter(is_active=True)
        serializer = MaterialSerializer(materials,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class MaterialDetail(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request,slug):
        materials = Material.objects.filter(is_active=True,slug=slug)
        serializer = MaterialSerializer(materials,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)










    
    
