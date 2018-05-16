from django.db import models
from django.utils import timezone


from ckeditor_uploader.fields import RichTextUploadingField

from taggit.managers import TaggableManager

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    category = TaggableManager(blank=True)
    title = models.CharField(max_length=200)
    description = RichTextUploadingField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

