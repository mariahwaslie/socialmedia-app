from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from tinymce.models import HTMLField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    bio = models.CharField(max_length=100, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # add a profile picture
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/profile_pic_blank.png')
    followers = models.ManyToManyField(User, related_name='following', blank=True, symmetrical=False)
    blocked =models.ManyToManyField(User, related_name='blocked_users', blank=True, symmetrical=False)

class Follow(models.Model):
    # person that wants to follow a user
    follower = models.OneToOneField(User, on_delete=models.CASCADE, related_name='follower')
    follower_following = models.ManyToManyField(User, related_name='followings', blank=True)