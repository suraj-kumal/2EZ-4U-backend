from datetime import datetime, timedelta, time
from django.conf import settings 
from django.http import Http404
from django.shortcuts import get_object_or_404,get_list_or_404


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,mixins
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.decorators import authentication_classes,permission_classes


from smartad.models import Location,Advertisement,AdvertisementSubCategory,AdvertisementLocation,AdvertisementTag,BannerType,Click,Impression,AdType
from smartad.serializers import LocationSerializer,AdvertisementSerializer,AdvertisementLocationSerializer,AdvertisementSubCategorySerializer,AdvertisementTagSerializer,BannerTypeSerializer,ImpressionSerializer,ClickSerializer,AdTypeDetailSerializer,AdvertisementTagBaseSerializer,AdTypeSerializer

# Create your views here.

class ListAdsByType(generics.GenericAPIView):
    """
    This view lists all ads of given type in detail
    """
    serializer_class = AdTypeDetailSerializer
    def get_queryset(self,ad_type_slug):
        try:
            ad_type = AdType.objects.filter(slug=ad_type_slug)
            return ad_type
        except AdType.DoesNotExist:
            raise Http404

    def get(self,request,ad_type_slug):
        ad_type = self.get_queryset(ad_type_slug=ad_type_slug)
        serializer = AdTypeDetailSerializer(ad_type,many=True,context={"request": request})
        if serializer.data:
            content = {'status':status.HTTP_200_OK,'data':serializer.data,'message':'success'}
            return Response(content)
        raise Http404

class ListAdType(generics.GenericAPIView):
    """
    This view lists all ads types
    """
    serializer_class = AdTypeSerializer
    def get_queryset(self):
        try:
            ad_type = AdType.objects.all()
            return ad_type
        except AdType.DoesNotExist:
            raise Http404

    def get(self,request):
        ad_type = self.get_queryset()
        serializer = AdTypeSerializer(ad_type,many=True)
        if serializer.data:
            content = {'status':status.HTTP_200_OK,'data':serializer.data,'message':'success'}
            return Response(content)
        raise Http404



class ListAdsByTag(generics.GenericAPIView):
    """
    This view lists all ads of given tags and type
    """
    serializer_class = AdvertisementSerializer
    # def get_ad_tag(self,tag,ad_type):
    #     try:
    #         ad_type = AdvertisementTag.objects.filter(tags__id=tag,advertisement__ad_type__id=ad_type)
    #         return ad_type
    #     except AdvertisementTag.DoesNotExist:
    #         raise Http404
    # def get_queryset(self,l):
    #     try:
    #         ads = Advertisement.objects.filter(id__in=l).order_by('-weight')
    #         return ads
    #     except Advertisement.DoesNotExist:
    #         return Http404

    # def get(self,request,tag,ad_type):
    #     ad_type = self.get_ad_tag(tag=tag,ad_type=ad_type)
    #     l = []
    #     for ad in ad_type:
    #         l.append(ad.advertisement.id)

    #     ad = self.get_queryset(l=l)
    #     serializer = AdvertisementSerializer(ad,many=True)
    #     if serializer.data:
    #         content = {'status':status.HTTP_200_OK,'data':serializer.data,'message':'success'}
    #         return Response(content)
    #     raise Http404




