from django.contrib import admin
from user import models

admin.site.register(models.UserProfile)
admin.site.register(models.Profile)
admin.site.register(models.Follow)

# Register your models here.
