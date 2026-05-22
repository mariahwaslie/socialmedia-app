from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from tinymce.models import HTMLField
from person.models import Category



PRIVACY_CHOICES = (
    ('followers', 'Followers'),
    ('public', 'Public'),
    ('only_me', 'Only me'),
)


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='author',default=None)
    tags = models.ManyToManyField(Category, related_name='post_tags',  blank=True, null=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')

    def __str__(self):
        return self.title

