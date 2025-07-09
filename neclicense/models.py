import uuid
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError

# Create your models here.
def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError(u'Error message, only PDF file allowed')
    
class Program(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=255)
    description = RichTextField(config_name='awesome_ckeditor',blank=True,null=True)
    logo = models.FileField(upload_to="uploads/%Y/%m/%d/")
    slug = models.SlugField(max_length=255,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Program.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Chapter(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=255)
    program = models.ForeignKey(Program,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    order_priority = models.IntegerField(default=0,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Chapter.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Topic(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=255)
    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['created_at']

    def __str__(self):
        return f'Topic:{self.title}||chapter:{self.chapter.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Topic.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Material(models.Model):
    STATUS_CHOICES = [
        ('published','PUBLISHED'),
        ('draft','Draft'),
    ]
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    content = RichTextField(config_name='awesome_ckeditor')
    pdf_file = models.FileField(upload_to="uploads/nec/%Y/%m/%d/",validators=[validate_file_extension],blank=True,null=True,default=None)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,related_name='materials')
    slug = models.SlugField(max_length=255,blank=True,null=True)
    status = models.CharField(choices = STATUS_CHOICES,default='draft',max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['created_at']

    def __str__(self):
        return self.content[:10]+"..."

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(str(self.uid))
        super().save(*args, **kwargs)
