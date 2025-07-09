from django.urls import path,include
from neclicense import views

urlpatterns = [
    path("program/list/",views.program_list,name="nec_program_list"),
    path("program/<slug:slug>",views.program_detail,name="nec_course_detail"),
    path("content/<slug:slug>/",views.content_detail_by_slug,name="content"),
    path('program/list/all/',views.ProgramList.as_view(),name='program_list_all'),
    path('topic/list/<slug:program_slug>/',views.TopicList.as_view(),name='topic_list'),
    path('program/detail/<slug:program_slug>/',views.ProgramDetail.as_view(),name='program_detail'),
    path('material/by/topic/<slug:topic_slug>/',views.MaterialByTopic.as_view(),name='material_by_topic'),

]