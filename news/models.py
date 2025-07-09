from django.db import models
import uuid

# Create your models here.

class NewsSite(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255,blank=True,null=True)
    def __str__(self):
        return self.name

class NewsAggregate(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    news_site = models.ForeignKey(NewsSite,on_delete=models.CASCADE)
    title = models.TextField()
    link = models.TextField()
    description = models.TextField()
    creator = models.TextField()
    publication_date = models.CharField(max_length=255)
    media_url = models.TextField()
    media_description = models.TextField()
    media_credit = models.TextField()
    categories = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['created_at']

    def __str__(self):
        return self.title


# class NyTimesModel(models.Model):
#     title = models.TextField()
#     link = models.TextField()
#     description = models.TextField()
#     creator = models.TextField()
#     publication_date = models.CharField(max_length=255)
#     media_url = models.TextField()
#     media_description = models.TextField()
#     media_credit = models.TextField()
#     categories = models.TextField()

#     def __str__(self):
#         return self.title

# class FoxNewsModel(models.Model):
#     title = models.TextField()
#     link = models.TextField()
#     description = models.TextField()
#     creator = models.TextField()
#     publication_date = models.CharField(max_length=255)
#     media_url = models.TextField()
#     media_description = models.TextField()
#     media_credit = models.TextField()
#     categories = models.TextField()

#     def __str__(self):
#         return self.title

# class PcMagModel(models.Model):
#     title = models.TextField()
#     link = models.TextField()
#     description = models.TextField()
#     creator = models.TextField()
#     publication_date = models.CharField(max_length=255)
#     media_url = models.TextField()
#     media_description = models.TextField()
#     media_credit = models.TextField()
#     categories = models.TextField()

#     def __str__(self):
#         return self.title

# class CnetModel(models.Model):
#     title = models.TextField()
#     link = models.TextField()
#     description = models.TextField()
#     creator = models.TextField()
#     publication_date = models.CharField(max_length=255)
#     media_url = models.TextField()
#     media_description = models.TextField()
#     media_credit = models.TextField()
#     categories = models.TextField()

#     def __str__(self):
#         return self.title
