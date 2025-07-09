from django.urls import path,include
from news import views

urlpatterns = [
    path("scrape00ef4e8d411f0f320818f3857a7a19a97d4984b1e5d850b09edde428b5531a95/",views.start_scrapper,name="start_scrapper"),
    path('top/five/',views.TopFiveNews.as_view(),name='top_five_news'),
    path("list/", views.news_list,name='news_list'),
    path("page/<str:uid>/", views.get_news,name='get_news'),
]