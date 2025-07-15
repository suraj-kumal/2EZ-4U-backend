from rest_framework import serializers

from smartad.models import BannerType,Advertisement,Location,AdvertisementLocation,AdvertisementSubCategory,AdvertisementTag,AdType,Impression,Click
from taggit.models import Tag


# define your serializers here..


class AdvertisementSerializer(serializers.ModelSerializer):
    banner_image = serializers.SerializerMethodField()
    class Meta:
        model = Advertisement
        exclude = ('created_at','updated_at','per_click_cost','start_date','stop_date',)
    
    def get_banner_image(self,obj):
        request = self.context.get('request')
        banner_image_url = obj.banner_image.url
        return request.build_absolute_uri(banner_image_url)

class AdTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdType 
        exclude = ('created_at','updated_at',)


class AdTypeDetailSerializer(serializers.ModelSerializer):
    advertisement = serializers.SerializerMethodField()
    class Meta:
        model = AdType
        exclude = ('created_at','updated_at',)
    def get_advertisement(self,obj):
        ad = Advertisement.objects.filter(ad_type__id=obj.id).order_by('-weight')
        serializer = AdvertisementSerializer(ad,many=True,context=self.context)
        return serializer.data

class BannerTypeSerializer(serializers.ModelSerializer):
    # advertisement = AdvertisementSerializer(many=True,read_only=True)
    advertisement = serializers.SerializerMethodField()
    class Meta:
        model = BannerType
        fields = '__all__'
    
    def get_advertisement(self,obj):
        ad = Advertisement.objects.filter(banner_type__id=obj.id).order_by('-weight')
        serializer = AdvertisementSerializer(ad,many=True,context=self.context)
        return serializer.data

class AdvertisementTagBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementTag
        exclude = ('created_at','updated_at')

class AdvertisementTagSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer()
    class Meta:
        model = AdvertisementTag
        exclude = ('created_at','updated_at')

class AdvertisementLocationSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer()
    class Meta:
        model = AdvertisementLocation
        fields = '__all__'

class AdvertisementSubCategorySerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer()
    class Meta:
        model = AdvertisementSubCategory
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ImpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Impression
        fields = '__all__'

class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = '__all__'


