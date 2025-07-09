from django.contrib.sitemaps import Sitemap
from neclicense.models import Program,Material
 
 
class ProgramSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Program.objects.all()

    def lastmod(self, obj):
        return obj.created_at
        
    def location(self,obj):
        return f'nec/exam/program/{obj.slug}'
    
class NecMaterialSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Material.objects.all()

    def lastmod(self, obj):
        return obj.created_at
        
    def location(self,obj):
        return f'nec/exam/content/{obj.topic.slug}'