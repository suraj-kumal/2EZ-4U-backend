from rest_framework import serializers
from content.models import *

class CourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseType
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    course_type = CourseTypeSerializer(read_only=True)
    class Meta:
        model = Subject 
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    class Meta:
        model = Chapter 
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    # chapter = ChapterSerializer(read_only=True)
    class Meta:
        model = Topic 
        fields = '__all__'

class ChapterDetailSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True,many=True)
    class Meta:
        model = Chapter
        fields = '__all__'
        
class MaterialSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)
    class Meta:
        model = Material
        fields= '__all__'

class YoutubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTube
        fields = '__all__'

class SeoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoContent
        fields = '__all__'