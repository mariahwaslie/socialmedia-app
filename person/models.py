from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from tinymce.models import HTMLField
from django.urls import reverse
from groups.models import Group

PRIVACY_CHOICES = (
    ('followers', 'Followers'),
    ('public', 'Public'),
    ('only_me', 'Only me'),
)
class Podcast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='podcast_user')
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='audio_files/')
    created_at = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='podcast_picture/')
    is_public = models.BooleanField(default=False)

class Category(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    likes = models.ManyToManyField(User, related_name='video_likes', blank=True)
    views = models.ManyToManyField(User, related_name='video_views', blank=True)
    tags=models.ManyToManyField(Category, related_name='tags', blank=True)
    saves=models.ManyToManyField(User, related_name='saves_video', blank=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    group= models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='group_videos')



    def __str__(self):
        return self.title

    def engagement_rating(self):
        likes = self.likes.count()
        saves= self.saves.count()
        comments = self.video_comments.count()
        return likes + saves + (comments*1.2)

    def get_absolute_url(self):
        return reverse('person:viewvideo', kwargs={'pk': self.user.id,'video_id':self.id, 'action_type':' '})


class Post(models.Model): # this is for your prayers
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    # description = models.TextField(blank=True)
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    views = models.ManyToManyField(User, related_name='views', blank=True)
    tags=models.ManyToManyField(Category, related_name='tag_post', blank=True)
    saves=models.ManyToManyField(User, related_name='post_saves', blank=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    group= models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='group_posts')

    def get_absolute_url(self):
        return reverse('person:viewpost', kwargs={'pk': self.user.id,'post_id':self.id, 'action_type':' '})


    def total_likes(self):
        return self.likes.count()


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='postimages/')
    created_at = models.DateTimeField(auto_now_add=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    likes = models.ManyToManyField(User, related_name='img_likes', blank=True)
    views = models.ManyToManyField(User, related_name='img_views', blank=True)
    tags_img=models.ManyToManyField(Category, related_name='tags_img', blank=True)
    saves=models.ManyToManyField(User, related_name='img_saves', blank=True)
    group= models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='group_image')


    def get_absolute_url(self):
        return reverse('person:viewimage',kwargs={'pk':self.user.id,'image_id':self.id, 'action_type':' ' })

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_blog', default=None)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    views = models.ManyToManyField(User, related_name='blog_views', blank=True)
    tags= models.ManyToManyField(Category, related_name='blog_tags', blank=True)
    saves = models.ManyToManyField(User, related_name='blog_saves', blank=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    group= models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='group_blogpost')


    def get_absolute_url(self):
        return reverse('person:viewblogpost',kwargs={'pk': self.id, 'action_type':' ' })


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
class CommentsImage(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
class CommentsVideos(models.Model):
    video = models.ForeignKey(video, on_delete=models.CASCADE,related_name='video_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)


def __str__(self):
        return self.title

class CommentsBlog(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

#
# # Main Board model
class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    images = models.ManyToManyField(Image, through='BoardImage',related_name='images_board' , blank=True)
    videos = models.ManyToManyField(video, through='BoardVideo',related_name='videos_board', blank=True)
    posts = models.ManyToManyField(Post, through='BoardPost',related_name='posts_board', blank=True)
    blogs = models.ManyToManyField(BlogPost, through='BoardBlogPost',related_name='blogs_board', blank=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('person:viewboard', kwargs={'username': self.user.id, 'board_id': self.id})

    def get_next_order(self):
        return (self.images.count()+self.videos.count()+self.posts.count()+self.blogs.count())


# Through models for ordering
class BoardImage(models.Model):
    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

class BoardVideo(models.Model):
    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    video = models.ForeignKey(video, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

class BoardPost(models.Model):
    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

class BoardBlogPost(models.Model):
    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']



# class Saves(models.Model):
#     PRIVACY_CHOICES = (
#         ('followers', 'Followers'),
#         ('public', 'Public'),
#         ('only_me', 'Only me'),
#     )
#     user= models.ForeignKey(User,on_delete=models.CASCADE)
#     images=models.ManyToManyField(Image, related_name='saved_imgs',blank=True)
#     videos= models.ManyToManyField(video,related_name='video_saves',blank=True)
#
# #




