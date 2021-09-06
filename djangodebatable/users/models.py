from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from datetime import datetime


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(blank=True, null=True)
    respecting = models.IntegerField(blank=True, null=True)
    respectedBy = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=False)
    ideology = models.CharField(max_length=50, default=0)
    searching = models.BooleanField(default=False)
    room = models.CharField(max_length=32, blank=True, null=True)
    topic = models.CharField(max_length=100, blank=True, null=True)
    style = models.CharField(max_length=100, blank=True, null=True)
    rating = models.SmallIntegerField(default=-1)
    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
    	return reverse("users:profile", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Report(models.Model):
    reporter = models.CharField(max_length=25)
    offender = models.CharField(max_length=25)
    date = models.CharField(default=datetime.now, max_length=100)
    profanity = models.BooleanField(default=False, blank=True)
    discrimination = models.BooleanField(default=False, blank=True)
    inappropriate = models.BooleanField(default=False, blank=True)
    sexual = models.BooleanField(default=False, blank=True)
    bot = models.BooleanField(default=False, blank=True)
    message = models.CharField(max_length=300, blank=True, default='')

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
