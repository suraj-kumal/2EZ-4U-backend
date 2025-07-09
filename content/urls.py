from django.urls import path,include
from content import views
app_name="content"
urlpatterns = [
    path("", views.index,name='home'),
    path("notice/",views.get_notice,name='get_notice'),
    path("about/us/",views.aboutus,name='aboutus'),
    path("subject/list/",views.subject_list,name="subject_list"),
    path("course/<slug:slug>",views.course_detail,name="course"),
    # path("content/<slug:slug>",views.content_detail,name="content"),
    path("content/<slug:slug>/",views.content_detail_by_slug,name="content"),
    path("ads.txt",views.get_ads_txt,name="ads_txt"),
    # for datascience tutorial
    path('datascience/',views.tutorial_home,name="tutorial_home"),
    path("datascience/<slug:slug>",views.tutorial_detail,name="datascience_home"),
    path("datascience/content/<slug:slug>/",views.tutorial_detail_by_slug,name="tutorial_detail"),

    # for engineering project
    path('engineering/project/',views.engineering_project_home,name='engineering_project'),
    path('engineering/project/<slug:slug>/',views.engineering_project_detail,name='engineering_project_detail'),

    # path('list/course/type/',views.CourseTypeList.as_view(),name='coursetype_list'),
    # path('course/type/detail/<slug:slug>/',views.CourseTypeDetail.as_view(),name='coursetype_detail'),
    path('list/subjects/',views.SubjectList.as_view(),name='subject_list'),
    path('list/youtube/',views.YouTubeList.as_view(),name='youtube_list'),
    path('topic/by/subject/<slug:subject_slug>/',views.TopicListBySubject.as_view(),name='topic_by_subject'),
    path('material/by/topic/<slug:topic_slug>/',views.MaterialByTopic.as_view(),name='material_by_topic'),
    path('subjects/detail/<slug:slug>/',views.SubjectDetail.as_view(),name='subject_detail'),
    path('seo/detail/<slug:course_slug>/',views.SeoDetail.as_view(),name='seo_detail'),
    # path('list/chapters/',views.ChapterList.as_view(),name='chapter_list'),
    # path('chapters/detail/<slug:slug>/',views.ChapterDetail.as_view(),name='chapter_detail'),
    # path('list/topics/',views.TopicList.as_view(),name='topic_list'),  
    # path('topics/detail/<slug:slug>/',views.TopicDetail.as_view(),name='topic_detail'),    
    # path('list/materials/',views.MaterialList.as_view(),name='material_list'),
    # path('materials/detail/<slug:slug>/',views.MaterialDetail.as_view(),name='material_detail'), 
]