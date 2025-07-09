"""tutorialsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from blog.sitemaps import ArticleSitemap
from content.sitemaps import SubjectSitemap, MaterialSitemap
from neclicense.sitemaps import ProgramSitemap, NecMaterialSitemap


sitemaps = {
    "blog": ArticleSitemap,
    "subjects": SubjectSitemap,
    "materials": MaterialSitemap,
    "programs": ProgramSitemap,
    "necmaterials": NecMaterialSitemap,
}
urlpatterns = [
    # path(
    #     "api/00ef4e8d411f0f320818f3857a7a19a97d4984b1e5d850b09edde428b5531a95/",
    #     admin.site.urls,
    # ),
    path("api/", include("content.urls")),
    path("news/", include("news.urls")),
    path("api/nec/exam/", include("neclicense.urls")),
    path("blog/", include("blog.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("contentadmin/", include("contentadmin.urls")),  # <-- Add this line
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
