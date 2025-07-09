from django.contrib import admin
from blog.models import Category,Article,Tag
# Register your models here.
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Article)
