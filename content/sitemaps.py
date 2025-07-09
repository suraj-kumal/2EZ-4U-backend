from django.contrib.sitemaps import Sitemap
from content.models import Material,Subject
 
 
class SubjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Subject.objects.all()

    def lastmod(self, obj):
        return obj.created_at
        
    def location(self,obj):
        return f'course/{obj.slug}'
    
class MaterialSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Material.objects.all()

    def lastmod(self, obj):
        return obj.created_at
        
    def location(self,obj):
        return f'content/{obj.topic.slug}'