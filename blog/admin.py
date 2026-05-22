# blog/admin.py
from django.contrib import admin
from django.contrib import messages
from django.conf import settings
from .models import Post
from django import forms


@admin.action(description='Check TinyMCE API Key')
def check_api_key(modeladmin, request, queryset):
    api_key = getattr(settings, 'TINYMCE_DEFAULT_CONFIG', {}).get('api_key', None)
    if api_key:
        messages.info(request, f'TinyMCE API Key is currently set.')
    else:
        messages.warning(request, 'TinyMCE API Key is not set in settings.py.')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    actions = [check_api_key]

admin.site.register(Post, PostAdmin)
