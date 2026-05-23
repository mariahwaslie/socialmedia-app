from django.contrib import admin
from .models import  *

# Register your models here.
admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(GroupCreationRequest)
admin.site.register(GroupRequest)
admin.site.register(Event)
admin.site.register(Location)
admin.site.register(ChurchCreationRequest)
# admin.py

from django.contrib import admin
from .models import Event
