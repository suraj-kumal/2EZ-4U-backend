from django.shortcuts import render
from blog.models import Category,Article,Tag
from content.models import Subject
# Create your views here.
def blog_list(request):
    blogs = Article.objects.all().order_by('-created_at')
    recent_blogs = Article.objects.all().order_by('created_at')[:3]
    subjects = Subject.objects.all()
    return render(request,'blog/blog_list.html',{'blogs':blogs,'recent_blogs':blogs,'subjects':subjects})

def blog_detail(request,slug):
    blog=None
    try:
        blog = Article.objects.get(slug=slug)
        tags = blog.tags.all()
    except Article.DoesNotExist:
        pass
    subjects = Subject.objects.all()
    return render(request,'blog/blog_content.html',{'blog':blog,'tags':tags,'subjects':subjects})
