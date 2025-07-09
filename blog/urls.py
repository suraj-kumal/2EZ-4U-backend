from django.urls import path,include
from blog import views

urlpatterns = [
    path("list/", views.blog_list,name='blog_list'),
    path("<slug:slug>/",views.blog_detail,name="blog_detail"),
]