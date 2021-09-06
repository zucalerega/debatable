from django.db import models
from django.utils import timezone
# Create your models here.
class Resource(models.Model):
    type = models.CharField(default='null', max_length=50)
    style = models.CharField(max_length=100, default='null')
    link = models.CharField(max_length=200, default='null')
    title = models.CharField(max_length=100, default='')
    content = models.CharField(max_length=1000000, default='')
    author = models.CharField(max_length=100, default='')
    published = models.DateTimeField(max_length=100, default=timezone.now)
    uses = models.IntegerField(default=0)
