from rest_framework import serializers
from neclicense.models import Program,Chapter,Topic,Material

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    subject = ProgramSerializer(read_only=True)
    class Meta:
        model = Chapter 
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    chapter = ChapterSerializer(read_only=True)
    class Meta:
        model = Topic 
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)
    class Meta:
        model = Material
        fields= '__all__'