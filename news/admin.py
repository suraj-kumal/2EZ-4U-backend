from django.contrib import admin
from news.models import NewsAggregate,NewsSite

class NewsAggregateAdmin(admin.ModelAdmin):
    list_display = ['news_site','title']

# Register your models here.
admin.site.register(NewsSite)
admin.site.register(NewsAggregate,NewsAggregateAdmin)
