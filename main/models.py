from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Choice(models.Model):
    title = models.CharField(max_length=500)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=65)
    lessons = models.IntegerField(default=0)
    rubric = models.ForeignKey(Choice, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='static')
    is_main = models.BooleanField(default=0, blank=True)
    show_count = models.IntegerField(default=0, blank=True)
    comment_count = models.IntegerField(default=0, blank=True)
    link = models.CharField(max_length=300, blank=True)
    description = models.CharField(max_length=2000)
    view = models.IntegerField(default=0, blank=True)
    short_description = models.CharField(max_length=200, blank=True)

    def get_absolute_url(self):
        return '/video/'

    def __str__(self):
        return self.title


class Shi(models.Model):
    title = models.CharField(max_length=300)
    time = models.DateTimeField()
    logo = models.ImageField(upload_to='static')
    view = models.IntegerField(default=0, blank=True)
    show_count = models.IntegerField(default=0, blank=True)
    short_description = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

    def get_absolute_url(self):
        return '/news/'

    def __str__(self):
        return self.title