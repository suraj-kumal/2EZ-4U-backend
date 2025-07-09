from django.contrib import admin
from content.models import Subject,Chapter,Topic,Material,Notice,YouTube,CourseType,SeoContent,EngineeringProject,EngineeringProjectCategory
from django.utils.html import mark_safe

# Register your models here.

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title','created_at']

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title','created_at']

class ChapterAdmin(admin.ModelAdmin):
    list_display = ['subject','title','order_priority','created_at']

class TopicAdmin(admin.ModelAdmin):
    list_display = ['subject_name','chapter','title','created_at']
    def subject_name(self,obj):
        return obj.chapter.subject.title
    
class SeoContentAdmin(admin.ModelAdmin):
    list_display = ['subject_name','title','created_at']
    def subject_name(self,obj):
        return obj.subject.title

class MaterialAdmin(admin.ModelAdmin):
    list_display = ['topic','content_value','created_at']
    def content_value(self,obj):
        return mark_safe(obj.content[:50])
    
class EngineeringProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['title','created_at']

class EngineeringProjectAdmin(admin.ModelAdmin):
    list_display = ['title','created_at']

admin.site.register(CourseType)
admin.site.register(YouTube)
admin.site.register(Notice,NoticeAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Chapter,ChapterAdmin)
admin.site.register(Topic,TopicAdmin)
admin.site.register(Material,MaterialAdmin)
admin.site.register(SeoContent,SeoContentAdmin)

admin.site.register(EngineeringProject,EngineeringProjectAdmin)
admin.site.register(EngineeringProjectCategory,EngineeringProjectCategoryAdmin)



