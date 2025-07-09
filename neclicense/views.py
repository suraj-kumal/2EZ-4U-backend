from django.shortcuts import render
from neclicense.models import Program,Chapter,Topic,Material
from content.models import Subject
# from blog.models import Article
from django.http import Http404,JsonResponse
from django.db.models import Prefetch
from content.serializers import MaterialSerializer,SubjectSerializer
from neclicense.serializers import ProgramSerializer,ChapterSerializer,TopicSerializer
import requests
import json
from bs4 import BeautifulSoup

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny

# Create your views here.

#API View

from rest_framework.permissions import BasePermission

class TokenAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.auth is not None
    

class ProgramList(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request):
        items = Program.objects.filter(is_active=True)
        serializer = ProgramSerializer(items,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ProgramDetail(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request,program_slug):
        items = Program.objects.filter(slug=program_slug)
        serializer = ProgramSerializer(items,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class TopicList(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request,program_slug):
        chapters = Chapter.objects.filter(program__slug=program_slug)
        data = []
        for chapter in chapters:
            topics = Topic.objects.filter(chapter=chapter)
            serializer = TopicSerializer(topics,many=True)
            data.append(serializer.data)
        return Response(data,status=status.HTTP_200_OK)

class MaterialByTopic(APIView):
    permission_classes = [TokenAuthenticated]
    def get(self,request,topic_slug):
        topic = Topic.objects.get(slug=topic_slug)
        material = Material.objects.get(topic=topic)
        serializer = MaterialSerializer(material)
        return Response(serializer.data,status=status.HTTP_200_OK)




def program_list(request):
    subjects = Subject.objects.filter(is_active=True)
    programs = Program.objects.filter(is_active=True)
    context_dict = {'programs':programs,'subjects':subjects}
    return render(request,'pages/programs.html',context=context_dict)




# def index(request):
#     try:
#         course_type = CourseType.objects.all()[0]
#     except CourseType.DoesNotExist:
#         raise Http404("Doesnot exists")
#     subjects = Subject.objects.filter(is_active=True,course_type=course_type)
#     you_tube = YouTube.objects.latest('created_at')
#     blogs = Article.objects.all().order_by('created_at')[:3]
#     context_dict = {'subjects':subjects,'you_tube':you_tube,'blogs':blogs}
#     return render(request,'pages/index.html',context=context_dict)

def program_detail(request,slug):
    try:
        subject = Program.objects.get(is_active=True,slug=slug)
    except Program.DoesNotExist:
        raise Http404("Course Doesnot exists")
    try:
        chapter_qs = Chapter.objects.filter(program=subject).order_by('order_priority')
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
        subjects = Program.objects.filter(is_active=True)
    except Exception as e:
        print(e)
        return render(request,'pages/pagenotfound.html')
    try:
        materials = list(Material.objects.all())
        prev_content = 0
        next_content = materials[1].topic.slug 
    except Exception as e:
        return render(request,'pages/pagenotfound.html')

    return render(request,'pages/program_content.html',context={'chapters_and_topics':chapter_topic,'initial_content':initial_content,'subject':subject,'subjects':subjects,'prev':prev_content,'next':next_content})

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
        topic = Topic.objects.get(uid = content.topic.uid)
    except Topic.DoesNotExist:
        data = {'content':'<h1>content not found</h1>'}
        return JsonResponse(data,safe=False)
    try:
        chapter = Chapter.objects.get(uid = topic.chapter.uid)
    except Topic.DoesNotExist:
        data = {'content':'<h1>content not found</h1>'}
        return JsonResponse(data,safe=False)
    try:
        subject = Program.objects.get(uid = chapter.program.uid)
    except Subject.DoesNotExist:
        data = {'content':'<h1>content not found</h1>'}
        return JsonResponse(data,safe=False)
    
    # try:
    #     subject = Subject.objects.get(is_active=True,slug=slug)
    # except Subject.DoesNotExist:
    #     raise Http404("Course Doesnot exists")
    try:
        chapter_qs = Chapter.objects.filter(program=subject).order_by('order_priority')
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
        subjects = Program.objects.filter(is_active=True)
    except Exception as e:
        print(e)
        return render(request,'pages/pagenotfound.html')
    try:
        materials = list(Material.objects.all())
        current_index = materials.index(content)
        prev_content = 0
        next_content = 0
        if current_index==0:
            prev_content = 0
            next_content = materials[1].topic.slug 
        elif current_index==len(materials)-1:
            next_content = 0
            prev_content = materials[current_index-1].topic.slug 
        else:
            prev_content = materials[current_index+1].topic.slug 
            next_content = materials[current_index-1].topic.slug 
    except Exception as e:
        print(e)
        return render(request,'pages/pagenotfound.html')
    
    return render(request,'pages/program_content_single.html',context={'chapters_and_topics':chapter_topic,'initial_content':initial_content,'subject':subject,'subjects':subjects,'content':content.content,'prev':prev_content,'next':next_content })
    




    
    
