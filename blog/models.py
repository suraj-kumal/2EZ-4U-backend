import uuid
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

class Tag(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    slug = models.TextField(blank=True,null=True)
    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "tags"
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Tag.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Category(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    slug = models.TextField(blank=True,null=True)
    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "categories"
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


def get_category():
    return Category.objects.get_or_create(name="data science")
class Article(models.Model):
    STATUS_CHOICES=[
        ('draft','Draft'),
        ('published','Published')
    ]
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.TextField()
    featured_image = models.FileField(upload_to="uploads/%Y/%m/%d/",blank=True,null=True)
    content = RichTextField(config_name='awesome_ckeditor')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=get_category)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    published_status = models.CharField(choices=STATUS_CHOICES,default='draft',max_length=255)
    published_at = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    slug = models.TextField(blank=True,null=True)
    tags = models.ManyToManyField(Tag)
    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "articles"
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
