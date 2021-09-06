from django.db import models
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
import random
import string
# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)
    auo = models.CharField(max_length=25, null=True)
    aut = models.CharField(max_length=1000, null=True)
    topic = models.CharField(max_length=25, null=True)
    group_room = models.BooleanField(default=False)
    def get_absolute_url(self):
        return reverse("chat:room", kwargs={"name": self.name})

class Message(models.Model):
    value = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    room = models.CharField(max_length=1000, default="default")
    sender = models.CharField(max_length=35, default='anon')

class Rating(models.Model):
    rater = models.CharField(max_length=25)
    recipient = models.CharField(max_length=25)
    rating = models.IntegerField(default=100)
    message = models.CharField(max_length=1000)
    date = models.CharField(default=datetime.now, max_length=100)
