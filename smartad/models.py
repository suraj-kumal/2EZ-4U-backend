import uuid 

from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.utils.text import slugify
from datetime import datetime

#from news.models import SubCategory,Category


# Create your models here.

class BannerType(models.Model):
    """
        ('300 X 100','Rectangle'),
        ('728 X 90','Leaderboard'),
        ('468 X 60', 'Full Banner'),
        ('250 X 250','Square'),
        ('120 X 600','Skysrapper'),
        ('320 X 50','Mobile Leaderboard'),
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,allow_unicode=True,max_length=255,blank=True,editable=False)
    width = models.IntegerField(verbose_name='banner width in pixels')
    height = models.IntegerField(verbose_name='banner height in pixels')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "banner_types"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        name = self.title
        slug_str = f"{name}-{datetime.now()}"
        self.slug = slugify(slug_str,allow_unicode=True)
        return super().save(*args, **kwargs)

class AdType(models.Model):
    """
    AdType lists different types of ads: island ad, mast ad, footer ad etc.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,allow_unicode=True,max_length=255,blank=True,editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "ad_types"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        name = self.title
        slug_str = f"{name}-{datetime.now()}"
        self.slug = slugify(slug_str,allow_unicode=True)
        return super().save(*args, **kwargs)


class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,allow_unicode=True,max_length=255,blank=True,editable=False)
    ad_type = models.ForeignKey(AdType,on_delete=models.CASCADE,related_name='advertisement')
    code = models.UUIDField(default = uuid.uuid4,editable = False)
    url = models.URLField(verbose_name='advertised url')
    weight = models.IntegerField(verbose_name='ad weightage',help_text='assign number 1,2 or 3  with 3>2>1ad with higher weight will be given more preferences above other while displaying ad.')
    per_click_cost = models.DecimalField(max_digits=10,decimal_places=3)
    banner_type = models.ForeignKey('BannerType',on_delete=models.CASCADE,related_name='advertisement')
    banner_image = models.ImageField(upload_to='uploads/advertisement/%Y/%m/%d')
    start_date = models.DateTimeField(default=timezone.now,verbose_name='start showing')
    stop_date = models.DateTimeField(default=timezone.now,verbose_name='start showing')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['weight']
        verbose_name_plural = "advertisements"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        name = self.title
        slug_str = f"{name}-{datetime.now()}"
        self.slug = slugify(slug_str,allow_unicode=True)
        return super().save(*args, **kwargs)

class AdvertisementTag(models.Model):
    advertisement = models.ForeignKey('Advertisement',on_delete=models.CASCADE,related_name='advertisement_tag')
    tags = TaggableManager(help_text="Enter space or comma seperated values ",related_name='advertisement_tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "advertisement_tags"

    def __str__(self):
        return self.advertisement.title

class Location(models.Model):
    name = models.CharField(max_length=255,verbose_name='location name')
    zipcode = models.CharField(max_length=10,verbose_name='zip code of location')
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AdvertisementLocation(models.Model):
    advertisement = models.ForeignKey('Advertisement',on_delete=models.CASCADE,related_name='advertisement_location')
    location = models.ManyToManyField(Location,related_name='advertisement_location')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "advertisement_location"

    def __str__(self):
        return self.advertisement.title

class AdvertisementSubCategory(models.Model):
    advertisement = models.ForeignKey('Advertisement',on_delete=models.CASCADE,related_name='advertisement_subcategory')
    #subcategory = models.ForeignKey('news.SubCategory',on_delete=models.CASCADE,blank=True,null=True,related_name='advertisement_subcategory')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "advertisement_subcategory"

    def __str__(self):
        return self.advertisement.title


class Impression(models.Model):
    """
    The Ad Impression Model will record every time the ad is loaded on a page
    """
    advertisement = models.ForeignKey('Advertisement', on_delete=models.CASCADE, verbose_name='Advertisement',related_name='impression')
    impression_date = models.DateTimeField(verbose_name='When', auto_now_add=True)
    source_ip = models.GenericIPAddressField(verbose_name='Source IP Address', null=True, blank=True)
    session_id = models.CharField(verbose_name='Source Session ID',max_length=40, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Ad Impressions'
    
    def __str__(self):
        return self.advertisement.title


class Click(models.Model):
    """
    The AdClick model will record every click that a add gets
    """
    advertisement = models.ForeignKey('Advertisement', on_delete=models.CASCADE, related_name='click')
    click_date = models.DateTimeField(auto_now_add=True)
    source_ip = models.GenericIPAddressField(verbose_name='Source IP Address', null=True, blank=True)
    session_id = models.CharField(verbose_name='Source Session ID',max_length=40, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Ad Clicks'

    def __str__(self):
        return self.advertisement.title












    
