# # playlistapp/urls.py

from django.urls import path
from . import views
#
urlpatterns = [
    path('create/', views.PlaylistCreateView.as_view(), name='create_playlist'),
    path('<int:playlist_id>/add/', views.add_to_playlist, name='add_to_playlist'),
    path('<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
]
