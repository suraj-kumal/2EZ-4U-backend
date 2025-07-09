from django.contrib import admin
from neclicense.models import Program,Chapter,Topic,Material
from django.utils.html import mark_safe

# Register your models here.

class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title','created_at']

class ChapterAdmin(admin.ModelAdmin):
    list_display = ['program','title','order_priority','created_at']

class TopicAdmin(admin.ModelAdmin):
    list_display = ['program_name','chapter','title','created_at']
    def program_name(self,obj):
        return obj.chapter.program.title

class MaterialAdmin(admin.ModelAdmin):
    list_display = ['topic','content_value','created_at']
    def content_value(self,obj):
        return mark_safe(obj.content[:50])

admin.site.register(Program,ProgramAdmin)
admin.site.register(Chapter,ChapterAdmin)
admin.site.register(Topic,TopicAdmin)
admin.site.register(Material,MaterialAdmin)


