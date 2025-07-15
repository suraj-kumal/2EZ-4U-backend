from django.contrib import admin
from smartad.models import Advertisement,BannerType,AdvertisementLocation,AdvertisementTag,AdvertisementSubCategory,Location,Impression,Click,AdType
from smartad.forms import AdvertisementForm,AdvertisementTagForm
# Register your models here.

class BannerTypeAdmin(admin.ModelAdmin):
    list_display = ('title','slug','width','height',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name','zipcode','latitude','longitude',)

class AdTypeAdmin(admin.ModelAdmin):
    list_display = ('title','slug','is_active',)

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title','get_ad_type','url','weight','per_click_cost',)
    form = AdvertisementForm
    
    def get_ad_type(self,obj):
        return obj.ad_type.title

class AdvertisementLocationAdmin(admin.ModelAdmin):
    list_display = ('get_advertisement','get_location',)
    
    def get_advertisement(self,obj):
        return obj.advertisement.title
    def get_location(self,obj):
        return list(obj.location.all())

class AdvertisementTagAdmin(admin.ModelAdmin):
    list_display = ('get_advertisement','get_tags',)
    form = AdvertisementTagForm
    def get_advertisement(self,obj):
        return obj.advertisement.title
    def get_tags(self,obj):
        return list(obj.tags.all())

class AdvertisementSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('get_advertisement','get_subcategory',)
    
    def get_advertisement(self,obj):
        return obj.advertisement.title
    def get_subcategory(self,obj):
        return obj.subcategory.name


class ImpressionReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ClickReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ImpressionAdmin(ImpressionReadOnlyAdminMixin, admin.ModelAdmin):
    exclude = ('id',)


class ClickAdmin(ClickReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('id',)
    

#read only models for all users

admin.site.register(Impression, ImpressionAdmin)
admin.site.register(Click,ClickAdmin)

admin.site.register(Advertisement,AdvertisementAdmin)
admin.site.register(BannerType,BannerTypeAdmin)
admin.site.register(AdType,AdTypeAdmin)
admin.site.register(Location,LocationAdmin)
admin.site.register(AdvertisementLocation,AdvertisementLocationAdmin)
admin.site.register(AdvertisementSubCategory,AdvertisementSubCategoryAdmin)
admin.site.register(AdvertisementTag,AdvertisementTagAdmin)


