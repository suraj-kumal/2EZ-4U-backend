from django.urls import path
from smartad import views

urlpatterns = [
    path('by/adtype/<str:ad_type_slug>',views.ListAdsByType.as_view(),name="list_ad_by_type"),
    path('list/ad/types/',views.ListAdType.as_view(),name='list_ad_types'),
    path('by/tags/<str:tag>/<int:ad_type>/',views.ListAdsByTag.as_view(),name="list_ad_by_tags"),

]