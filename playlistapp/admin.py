# playlistapp/admin.py
from django.contrib import admin
from .models import Playlist, PlaylistItem
from person.models import video, Category  # Import other models if needed


admin.site.register(Playlist)
admin.site.register(PlaylistItem)
