from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
	username = models.CharField(max_length=25)
	bio = models.TextField(blank=True, null=True)
	respecting = models.IntegerField(blank=True, null=True)
	respectedBy = models.IntegerField(blank=True, null=True)
	active = models.BooleanField(default=False)
	ideology =  models.CharField(max_length=50, blank=True, null=True)

	def get_absolute_url(self):
		return reverse("profiles:profile-detail", kwargs={"id": self.id})
