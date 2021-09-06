from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=250)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs={'pk':self.pk})

class Like(models.Model):
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actor')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    action = models.BooleanField()
