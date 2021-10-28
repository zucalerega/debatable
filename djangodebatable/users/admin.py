from django.contrib import admin
from .models import Profile, Report, Follow, Feedback
# Register your models here.

admin.site.register(Profile)
admin.site.register(Report)
admin.site.register(Follow)
admin.site.register(Feedback)
