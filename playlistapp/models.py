from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from person.models import video,Category
# Create your models here.

PRIVACY_CHOICES = (
    ('followers', 'Followers'),
    ('public', 'Public'),
    ('only_me', 'Only me'),
)
# class Podcast(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100, blank=True)
#     description = models.TextField(blank=True)
#     audio_file = models.FileField(upload_to='audio_files/')
#     created_at = models.DateTimeField(auto_now_add=True)
#     picture = models.ImageField(upload_to='podcast_picture/')
#     is_public = models.BooleanField(default=False)
class Playlist(models.Model):
    PRIVACY_CHOICES = (
        ('followers', 'Followers'),
        ('public', 'Public'),
        ('only_me', 'Only me'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    tags=models.ManyToManyField(Category, blank=True)
    videos = models.ManyToManyField(video,through='PlaylistItem', blank=True)

    def __str__(self):
        return self.title

class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='playlist_video_items')
    video = models.ForeignKey(video, on_delete=models.CASCADE, related_name='playlist_videos')
    order = models.IntegerField(default=0)

    class Meta:
        unique_together = ('playlist', 'video')
        ordering = ['order']

    def __str__(self):
        return f"{self.playlist.title} - {self.video.title}"