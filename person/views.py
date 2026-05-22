import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from person.forms import *
# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from person.models import *
import time
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.auth.views import LogoutView
from notifications.signals import notify
from django.http import JsonResponse
from notifications.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from user.models import *
from .utils import *
import blog.models as blog_models
from .video_utils import find_similar_videos as videos_find_similar_videos, find_similar_images_to_video, \
    find_similar_posts_to_video as find_prayers
from .images_utils import find_similar_images_to_image, find_similar_videos_to_image, \
    find_similar_posts_to_image as find_similar_p
from .post_utils import find_similar_posts_to_post, find_similar_blogposts_to_post


# from django.contrib.auth.models import AnonymousUser

@login_required
def notifications_list(request):
    # Retrieve notifications for the logged-in user
    notifications = Notification.objects.filter(recipient=request.user)

    # Prepare the data to be returned
    data = [
        {
            'verb': n.verb,
            'description': n.description,
            'timestamp': n.timestamp.isoformat()  # Convert timestamp to ISO format for JSON compatibility
        }
        for n in notifications
    ]

    # Return the data as a JSON response
    return JsonResponse(data, safe=False)


# def get_redirect_url(self, *args, **kwargs):
# @login_required

# this will create a prayer
class CreatePost(CreateView, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'post.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        for follower in self.request.user.following.all():
            notify.send(
                self.request.user,
                recipient=follower.user,
                verb='new prayer',
                description=f'{self.request.user} created a new prayer'
            )
        return response

    def get_success_url(self):

        # Ensure the correct parameters are being passed to reverse_lazy
        return reverse_lazy('person:follow_unfollow_user', kwargs={
            'username': self.request.user,
            'action_type': ' ',
            # Assuming post_id refers to the post ID
        })

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['profile'] = Profile.objects.filter(user=self.request.user).values('bio', 'profile_picture').first()
    #     return context


class UploadVideo(CreateView, LoginRequiredMixin):
    model = video
    form_class = VideoForm
    template_name = 'upload.html'
    success_url = reverse_lazy('user:myvids')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        for follower in self.request.user.following.all():
            notify.send(
                self.request.user,
                recipient=follower.user,
                verb='new video',
                description=f'{self.request.user} created a new video'
            )

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(user=self.request.user).values('bio', 'profile_picture').first()
        return context

    def get_success_url(self):
        return redirect('user:profile').url


class CreatePodcast(CreateView, LoginRequiredMixin):
    model = Podcast
    template_name = 'create_podcast.html'
    form_class = PodcastForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_about'] = Profile.objects.filter(user=self.request.user).values('bio', 'profile_picture').first()

        return context


class ViewPodcats(TemplateView, LoginRequiredMixin):
    template_name = 'podcast.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_about'] = Profile.objects.filter(user=self.request.user).values('bio', 'profile_picture').first()
        context['podcasts'] = Podcast.objects.filter(user=self.request.user).values('title', 'description',
                                                                                    'created_at', 'audio_file')
        return context


def follow_unfollow(request, username, action_type):
    # user with page username <str:username>
    target_user = get_object_or_404(User, username=username)
    # user=get_object_or_404(User, pk=request.user.pk)
    # user_follow =Follow.objects.get_or_create(follower=user)
    # current profile pagepy
    boards = Board.objects.filter(user=target_user)
    p = Profile.objects.get(user=target_user)
    followers = p.followers.all()
    following = target_user.following.all()

    profile_list = (Profile.objects.filter(followers=target_user).exclude(user=target_user))
    videos = video.objects.filter(user=target_user)
    posts = Post.objects.filter(user=target_user)
    audios = Podcast.objects.filter(user=target_user)
    images = Image.objects.filter(user=target_user)
    blogs = BlogPost.objects.filter(created_by=target_user)
    saved_vids = video.objects.filter(saves=target_user)
    saved_images = Image.objects.filter(saves=target_user)
    saved_posts = Post.objects.filter(saves=target_user)
    saved = list(saved_vids) + list(saved_images) + list(saved_posts)
    all = list(posts) + list(videos) + list(audios) + list(images) + list(blogs)
    video_list = list(videos)
    # items_by_date = sorted(
    #     all,
    #     key=lambda k: k['created_at'],
    #     reverse=True
    # )
    response_data = {}
    if request.user.is_authenticated:

        followers = p.followers.all()

        if action_type == 'follow':
            if request.user in followers:
                target_user = get_object_or_404(User, username=username)
                target_user.profile.followers.remove(request.user)
                response_data['follows'] = False
            else:
                target_user.profile.followers.add(request.user)
                response_data['follows'] = True
                notify.send(
                    request.user,
                    recipient=target_user,
                    verb='new follower',
                    description=f'{request.user} followed you',
                )
            response_data['total_follows'] = target_user.profile.followers.count()
            return JsonResponse(response_data)
        # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        elif action_type == 'block':
            if target_user in request.user.profile.blocked.all():
                request.user.profile.blocked.remove(target_user)
                response_data['blocked_user'] = False
                # return JsonResponse(response_data)
            else:
                request.user.profile.blocked.add(target_user)
                if target_user in request.user.profile.followers.all():
                    request.user.profile.followers.remove(target_user)

                response_data['blocked_user'] = True
                # return JsonResponse(response_data)
        # return JsonResponse(response_data)

            return JsonResponse(response_data)
        # elif action_type == 'follow' or action_type == 'block':
        #     return redirect('person:follow_unfollow_user',
        #                     kwargs={'username': username, 'action_type': action_type})

        # elif action_type == 'follow':
        #     return redirect('person:follow_unfollow_user',
        #                         kwargs={'username': username, 'action_type': action_type })

        #     if target_user.profile.followers.filter(id=request.user.id).exists():
        #         # request.user.profile.following.remove(target_user)
        #         target_user.profile.followers.remove(request.user)
        #         response_data['follows'] = False
        #     else:
        #         # request.user.profile.following.add(target_user)
        #         target_user.profile.followers.add(request.user)
        #         response_data['follows'] = True
        #     response_data['total_follows'] = target_user.profile.followers.count()
        # if request.is_ajax():
        #     return JsonResponse(response_data)
        # else:
        #     return redirect('person:viewpost',kwargs={'post_id':post_id,'username':target_user.username})

    return render(request,
                  'follow.html',
                  {"profile": p,
                   'target_user': target_user,
                   'followers': followers,
                   'profile_list': profile_list,
                   'videos': videos,
                   'posts': posts,
                   'items_by_date': all,
                   'video_list': video_list,
                   'images': images,
                   'saved_vids': saved_vids,
                   'saved_images': saved_images,
                   'saved': saved,
                   'saved_posts': saved_posts,
                   'boards': boards,
                   'blogs': blogs, 'following': following})


class CreateImage(CreateView, LoginRequiredMixin):
    model = Image
    template_name = 'uploadImage.html'
    form_class = ImageForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        channel_layer = get_channel_layer()

        # Send a real-time notification to the Redis channel
        async_to_sync(channel_layer.group_send)(
            'notifications',  # Ensure this matches your WebSocket group name
            {
                'type': 'send_notification',
                'message': f'{self.request.user.username} has uploaded an image: {self.object.title}'
            }
        )

        for follower in self.request.user.following.all():
            notify.send(
                self.request.user,
                recipient=follower.user,
                verb='new Image',
                description=f'{self.request.user} uploaded a new Image'
            )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context
    def get_success_url(self):
        return reverse_lazy('person:follow_unfollow_user', kwargs={'username': self.request.user.username,
                                                       'action_type': ' '})



# @login_required
# def commentsForm(request,post):
#     if request.method == 'POST':
#         form = CommentsForm(request.POST,request.FILES)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             # comment.body= form.cleaned_data['body']
#             comment.user = request.user
#             comment.post = post
#             comment.save()
#             return HttpResponseRedirect(reverse_lazy('person:createimage'))
def viewitem(request, post_id, pk, action_type):
    post = get_object_or_404(Post, id=post_id)
    target_user = get_object_or_404(User, pk=pk)
    blogs = BlogPost.objects.filter(created_by=target_user)
    #
    if request.user.is_authenticated:
        boards = Board.objects.filter(user=request.user)

    #     profile = request.user.profile
    #     username = request.user.username
    else:
        boards = None
        profile = None
        username = None
        # show profile picture in the top left corner
    comments = Comments.objects.filter(post=post).order_by('date')
    all_post = Post.objects.filter(user=target_user)
    all_vids = video.objects.filter(user=target_user)
    all_images = Image.objects.filter(user=target_user)
    alls = list(all_post) + list(all_vids) + list(all_images) + list(blogs)
    # items_by_date = sorted(
    #     alls,
    #     key=lambda k: k['created_at'],
    #     reverse=True
    # )
    response_data = {}
    if request.user.is_authenticated:
        if request.user not in post.views.all():
            post.views.add(request.user)
        # liking a post
        if action_type == 'like':
            post = get_object_or_404(Post, id=post_id)

            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
                response_data['liked'] = False
            else:
                post.likes.add(request.user)
                response_data['liked'] = True
                notify.send(
                    request.user,
                    recipient=post.user,
                    verb='post liked',
                    description='{} liked {}'.format(request.user, post.title),
                )
            response_data['total_likes'] = post.total_likes()
        elif action_type == 'follow':
            if target_user.profile.followers.filter(id=request.user.id).exists():
                target_user.profile.followers.remove(request.user)
                response_data['follows'] = False
            else:
                target_user.profile.followers.add(request.user)
                response_data['follows'] = True
                notify.send(
                    request.user,
                    recipient=post.user,
                    verb='new follower',
                    description='{} followed you'.format(request.user),
                )
            response_data['total_follows'] = target_user.profile.followers.count()
            # if request.is_ajax():
            #     return JsonResponse(response_data)
            # else:
            #     return redirect('person:viewpost',kwargs={'post_id':post_id,'username':target_user.username})
            #
        elif action_type == 'save':
            post = get_object_or_404(Post, id=post_id)
            if post.saves.filter(id=request.user.id).exists():
                response_data['saved'] = True

            else:
                post.saves.add(request.user)
                notify.send(
                    request.user,
                    recipient=post.user,
                    verb='post saved',
                    description='{} saved {}'.format(request.user, post.title),
                )
                response_data['saved'] = True
        elif Board.objects.filter(user=request.user, title=action_type).exists():
            board = get_object_or_404(Board, user=request.user, title=action_type)
            post = get_object_or_404(Post, id=post_id)
            if BoardPost.objects.filter(board=board, post=post).exists():
                response_data['saved'] = True
            else:
                next = board.get_next_order()
                BoardPost.objects.create(board=board, post=post, order=next)
                notify.send(
                    request.user,
                    recipient=post.user,
                    verb='post saved',
                    description='{} saved {} to board'.format(request.user, post.title),
                )
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(response_data)
        elif action_type == 'like' or action_type == 'follow' or action_type == 'save' or Board.objects.filter(
                user=request.user, title=action_type).exists():
            return redirect('person:viewpost',
                            kwargs={'post_id': post_id, 'pk': post.user.pk, 'action_type': action_type})

    all_posts = Post.objects.all()
    all_blogposts = blog_models.Post.objects.all()
    all_blogs = BlogPost.objects.all()
    all_videos = video.objects.all()
    similar_post = find_similar_posts_to_post(post_id)

    # Get similar blogposts
    similar_blogposts = find_similar_blogposts_to_post(post, all_blogposts)
    similar_blogs = find_similar_blogposts_to_post(post, all_blogs)
    similar_images = find_similar_images_imgpost(post_id)
    # similar_images = get_similar_images(post, all_images)
    similar_videos = find_similar_videos_blogpost(post)

    combined_results = []
    # Add images with similarity scores
    for img, score in similar_images:
        combined_results.append({'type': 'image', 'item': img, 'score': score})

    # Add videos with similarity scores
    for vid, score in similar_videos:
        combined_results.append({'type': 'video', 'item': vid, 'score': score})

    # Add prayers with similarity scores
    for prayer, score in similar_post:
        combined_results.append({'type': 'prayer', 'item': prayer, 'score': score})

    # Add blog posts with similarity scores
    for blogpost, score in similar_blogposts:
        combined_results.append({'type': 'blogpost', 'item': blogpost, 'score': score})

    # Add blogs with similarity scores
    for blog, score in similar_blogs:
        combined_results.append({'type': 'blog', 'item': blog, 'score': score})

    # Sort combined results by similarity score in descending order
    sorted_results = sorted(combined_results, key=lambda x: x['score'], reverse=True)
    ws_url = f'ws://{request.get_host()}/ws/comments/{post_id}/'

    context = {
        'post': post,
        # 'profile': profile,
        'comments': comments,
        'target_user': target_user,
        'all_posts': all_post,
        'all_vids': all_vids,
        'all_images': all_images,
        'items_by_date': alls,
        'boards': boards,
        'blogs': blogs,
        'ws_url': ws_url,
        'related_posts': sorted_results,
        'similar_images': similar_images,
        'similar_videos': similar_videos,
        'followers': post.user.profile.followers.all()
    }

    return render(request, 'viewpost.html', context)


def viewvideo(request, pk, video_id, action_type=None):
    target_user = get_object_or_404(User, pk=pk)
    vid = get_object_or_404(video, id=video_id)
    is_in_boardss = 'save to board'
    if request.user.is_authenticated:
        profile = request.user.profile
        boards = Board.objects.filter(user=request.user)
        for board in boards:
            if vid in board.videos.all():
                is_in_boardss = f' saved to {board.title}'
                break
            else:
                is_in_boardss = 'save to board'
    else:
        boards = []
        profile = None

    blogs = BlogPost.objects.filter(created_by=target_user)
    all_post = Post.objects.filter(user=target_user)
    all_vids = video.objects.filter(user=target_user)
    all_images = Image.objects.filter(user=target_user)
    alls = list(all_post) + list(all_vids) + list(all_images) + list(blogs)

    response_data = {}
    comment = CommentsVideos.objects.filter(video=vid).order_by('date')
    is_in_boardss = 'save to board'
    if request.user.is_authenticated:
        boards = Board.objects.filter(user=request.user)

        if request.user not in vid.views.all():
            vid = get_object_or_404(video, id=video_id)
            if request.user.is_authenticated:
                vid.views.add(request.user)

        if action_type == 'like':
            vid = get_object_or_404(video, id=video_id)

            if vid.likes.filter(id=request.user.id).exists():
                vid.likes.remove(request.user)
                response_data['liked'] = False
            else:
                vid.likes.add(request.user)
                response_data['liked'] = True
                notify.send(
                    request.user,
                    recipient=vid.user,
                    verb='post liked',
                    description='{} liked {}'.format(request.user, vid.title),
                )
            response_data['total_likes'] = vid.likes.count()
        elif action_type == 'follow':
            if request.user in target_user.profile.followers.all():
                target_user.profile.followers.remove(request.user)
                response_data['follows'] = False
            else:
                target_user.profile.followers.add(request.user)
                response_data['follows'] = True
                notify.send(
                    request.user,
                    recipient=vid.user,
                    verb='new follower',
                    description='{} followed you'.format(request.user),
                )
            response_data['total_follows'] = target_user.profile.followers.count()
        elif action_type == 'save':
            vid = get_object_or_404(video, id=video_id)
            if vid.saves.filter(id=request.user.id).exists():
                notify.send(
                    request.user,
                    recipient=vid.user,
                    verb='post saved',
                    description='{} saved {}'.format(request.user, vid.title),
                )
                response_data['saved'] = True

            else:
                vid.saves.add(request.user)
                notify.send(
                    request.user,
                    recipient=vid.user,
                    verb='post saved',
                    description='{} saved {}'.format(request.user, vid.title),
                )
                response_data['saved'] = True
        elif Board.objects.filter(user=request.user, title=action_type).exists() and request.user:
            print('action type ' + action_type)
            board = get_object_or_404(Board, user=request.user, title=action_type)
            vid = get_object_or_404(video, id=video_id)

            if BoardVideo.objects.filter(board=board, video=vid).exists():
                response_data['saved'] = True
            else:
                next_order = board.get_next_order()
                BoardVideo.objects.create(board=board, video=vid, order=next_order)
                notify.send(
                    request.user,
                    recipient=vid.user,
                    verb='post saved',
                    description='{} saved {} to board'.format(request.user, vid.title),
                )
                response_data['saved'] = True

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(response_data)
        elif action_type == 'like' or action_type == 'follow' or action_type == 'save' or Board.objects.filter(
                user=request.user, title=action_type).exists():
            return redirect('person:viewpost',
                            kwargs={'video_id': video_id, 'pk': target_user.id, 'action_type': action_type})
    ws_url = f'ws://{request.get_host()}/ws/comments/{vid.id}/'

    similar_videos = videos_find_similar_videos(vid.id)
    similar_images = find_similar_images_to_video(vid.id)
    similar_prayers = find_prayers(vid.id, Post.objects.all())
    similar_blogposts = find_prayers(vid.id, BlogPost.objects.all())
    similar_blogs = find_prayers(vid.id, blog_models.Post.objects.all())

    combined_results = []
    # Add images with similarity scores
    for img, score in similar_images:
        combined_results.append({'type': 'image', 'item': img, 'score': score})

    # Add videos with similarity scores
    for vid, score in similar_videos:
        combined_results.append({'type': 'video', 'item': vid, 'score': score})

    # Add prayers with similarity scores
    for prayer, score in similar_prayers:
        combined_results.append({'type': 'prayer', 'item': prayer, 'score': score})

    # Add blog posts with similarity scores
    for blogpost, score in similar_blogposts:
        combined_results.append({'type': 'blogpost', 'item': blogpost, 'score': score})

    # Add blogs with similarity scores
    for blog, score in similar_blogs:
        combined_results.append({'type': 'blog', 'item': blog, 'score': score})

    # Sort combined results by similarity score in descending order
    sorted_results = sorted(combined_results, key=lambda x: x['score'], reverse=True)

    context = {
        'video': video.objects.get(id=video_id),
        'profile': profile,
        'comment': comment,
        'target_user': target_user,
        'all_posts': all_post,
        'all_vids': all_vids,
        'all_images': all_images,
        'items_by_date': alls,
        'boards': boards,
        # 'is_in_boards': is_in_boards,
        'ws_url': ws_url,
        'related_posts': sorted_results,
        'followers': video.objects.get(id=video_id).user.profile.followers.all(),
        'is_in_board': is_in_boardss
        # 'similar_videos': similar_videos,
        # 'similar_images': similar_images,
        # 'similar_blogpost': similar_blogpost,
        # 'similar_blog':similar_blog
    }

    return render(request, 'viewvideo.html', context)


def viewimage(request, pk, image_id, action_type=None):
    image = get_object_or_404(Image, id=image_id)
    if request.user.is_authenticated:
        profile = request.user.profile
        boards = Board.objects.filter(user=request.user)
    else:
        profile = None
        boards = []
    target_user = get_object_or_404(User, pk=pk)

    blogs = BlogPost.objects.filter(created_by=target_user)
    comment = CommentsImage.objects.filter(image=image).order_by('date')
    all_post = Post.objects.filter(user=target_user)
    all_vids = video.objects.filter(user=target_user)
    all_images = Image.objects.filter(user=target_user)
    alls = list(all_post) + list(all_vids) + list(all_images) + list(blogs)
    response_data = {}
    # adds a view when user visits the page
    if request.user.is_authenticated:
        if request.user not in image.views.all():
            image.views.add(request.user)
        if action_type == 'like':
            image = get_object_or_404(Image, id=image_id)

            if image.likes.filter(id=request.user.id).exists():
                image.likes.remove(request.user)
                response_data['liked'] = False
            else:
                image.likes.add(request.user)
                response_data['liked'] = True
                notify.send(
                    request.user,
                    recipient=image.user,
                    verb='post liked',
                    description='{} liked {}'.format(request.user, image.title),
                )
            response_data['total_likes'] = image.likes.count()
        elif action_type == 'follow':
            if request.user in target_user.profile.followers.all():
                target_user.profile.followers.remove(request.user)
                response_data['follows'] = False
            else:
                target_user.profile.followers.add(request.user)
                response_data['follows'] = True
                notify.send(
                    request.user,
                    recipient=image.user,
                    verb='new follower',
                    description='{} followed you'.format(request.user),
                )
            response_data['total_follows'] = target_user.profile.followers.count()
        elif action_type == 'save':
            image = get_object_or_404(Image, id=image_id)
            if image.saves.filter(id=request.user.id).exists():
                response_data['saved'] = True
            else:
                image.saves.add(request.user)
                notify.send(
                    request.user,
                    recipient=image.user,
                    verb='post saved',
                    description='{} saved {}'.format(request.user, image.title),
                )
                response_data['saved'] = True
        elif Board.objects.filter(user=request.user, title=action_type).exists():
            board = get_object_or_404(Board, user=request.user, title=action_type)
            image = get_object_or_404(Image, id=image_id)

            if BoardImage.objects.filter(board=board, image=image).exists():
                response_data['saved'] = True
            else:
                next_order = board.get_next_order()
                boardimage = BoardImage.objects.create(board=board, image=image, order=next_order)
                # board.images.add(image)
                notify.send(
                    request.user,
                    recipient=image.user,
                    verb='image saved',
                    description='{} saved {} to board'.format(request.user, image.title),
                )
                response_data['saved'] = True
                return JsonResponse(response_data)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(response_data)
        elif action_type == 'like' or action_type == 'follow' or action_type == 'save' or Board.objects.filter(
                user=request.user, title=action_type).exists():
            return redirect('person:viewpost',
                            kwargs={'image_id': image_id, 'pk': target_user.id, 'action_type': action_type})
    ws_url = f'ws://{request.get_host()}/ws/comments/{image.id}/'
    similar_images = find_similar_images_to_image(image_id)
    similar_videos = find_similar_videos_to_image(image_id)
    similar_prayers = find_similar_p(image_id, Post.objects.all())
    similar_blogposts = find_similar_p(image_id, BlogPost.objects.all())
    similar_blogs = find_similar_p(image_id, blog_models.Post.objects.all())

    combined_results = []
    # Add images with similarity scores
    for img, score in similar_images:
        combined_results.append({'type': 'image', 'item': img, 'score': score})

    # Add videos with similarity scores
    for vid, score in similar_videos:
        combined_results.append({'type': 'video', 'item': vid, 'score': score})

    # Add prayers with similarity scores
    for prayer, score in similar_prayers:
        combined_results.append({'type': 'prayer', 'item': prayer, 'score': score})

    # Add blog posts with similarity scores
    for blogpost, score in similar_blogposts:
        combined_results.append({'type': 'blogpost', 'item': blogpost, 'score': score})

    # Add blogs with similarity scores
    for blog, score in similar_blogs:
        combined_results.append({'type': 'blog', 'item': blog, 'score': score})

    # Sort combined results by similarity score in descending order
    sorted_results = sorted(combined_results, key=lambda x: x['score'], reverse=True)

    context = {
        'image': image,
        'profile': profile,
        'comment': comment,
        'target_user': target_user,
        'all_posts': all_post,
        'all_vids': all_vids,
        'all_images': all_images,
        'items_by_date': alls,
        'boards': boards,
        'blogs': blogs,
        'ws_url': ws_url,
        'related_posts': sorted_results,
        'followers': image.user.profile.followers.all(),
        # 'similar_images': similar_images,
        # 'similar_blogposts': similar_blogposts,
        # 'similar_blogs': similar_blogs,
    }
    return render(request, 'viewimage.html', context)


@require_POST
def submit_video_comment(request, id):
    if request.method == 'POST':
        form = CommentsVideoForm(data=request.POST)
        if form.is_valid():
            vid = video.objects.get(id=id)
            comment = form.save(commit=False)
            comment.user = request.user
            comment.video = vid
            comment.parent = None
            comment.save()

            notify.send(
                request.user,
                recipient=vid.user,
                verb='{} commented on {}'.format(comment.user, vid.title),
                description=f'{comment.body}'
            )
            # Prepare the data to send back to the client
            if comment.user.profile.profile_picture.url:
                profile_picture = comment.user.profile.profile_picture.url
            else:
                profile_picture = '/media/base/profile_pic_blank.png'
            response_data = {
                'success': True,
                'comment': comment.body,
                'username': comment.user.username,
                'profile_picture': profile_picture,
            }

            return JsonResponse(response_data)

        else:
            return JsonResponse({'success': False, 'error': 'Form is not valid'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@require_POST
def submit_comment(request, id):
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, id=id)
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            if post:
                notify.send(
                    request.user,
                    recipient=post.user,
                    verb='commented on your post',
                    description=comment.body,
                    # action_object=comment,
                    timestamp=timezone.now()
                )

            # Prepare the data to send back to the client
            response_data = {
                'success': True,
                'comment': comment.body,
                'username': comment.user.username,
                'profile_picture': comment.user.profile.profile_picture.url,
            }

            return JsonResponse(response_data)
        else:
            return JsonResponse({'success': False, 'error': 'Form is not valid'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@require_POST
def submit_image_comment(request, id):
    if request.method == 'POST':
        form = CommentImageForm(data=request.POST)
        if form.is_valid():
            image = get_object_or_404(Image, id=id)
            comment = form.save(commit=False)
            comment.user = request.user
            comment.image = image
            comment.save()

            notify.send(
                request.user,
                recipient=image.user,
                verb='{} commented on {}'.format(comment.user, image.title),
                description=f'{comment.body}'
            )
            # Prepare the data to send back to the client
            if comment.user.profile.profile_picture.url:
                profile_picture = comment.user.profile.profile_picture.url
            else:
                profile_picture = 'base/profile_pic_blank.png'
            response_data = {
                'success': True,
                'comment': comment.body,
                'username': comment.user.username,
                'profile_picture': profile_picture,
            }

            return JsonResponse(response_data)

        else:
            return JsonResponse({'success': False, 'error': 'Form is not valid'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
# class ViewItems(View,LoginRequiredMixin):
#    def post(self,request,action_type,post_id,username):
#        response_data ={}
#        if action_type == 'like':
#             post = get_object_or_404(Post,id=post_id)
#
#             if post.likes.filter(id=request.user.id).exists():
#                 post.likes.remove(request.user)
#                 response_data['likes'] = False
#             else:
#                 post.likes.add(request.user)
#                 response_data['liked'] = True
#             response_data['total_likes'] = post.total_likes()
#        elif action_type == 'follow':
#            post = get_object_or_404(Post,id=post_id)
#            if post.follows.filter(id=request.user.id).exists():
#                post.follows.remove(request.user)
#                response_data['follows'] = False
#            else:
#                post.follows.add(request.user)
#        if request.is_ajax():
#            return JsonResponse(response_data)
#        if action_type =='like':
#            return redirect('person:viewpost',post_id=post_id)
def following_page(request):
    posts = []
    videos = []
    images = []
    blog_posts = []
    if request.user:
        user = request.user
        profile = Profile.objects.get(user=user)
        following = Profile.objects.filter(followers=user)
        for follows in following:
            posts += Post.objects.filter(user=follows.user)
            videos += video.objects.filter(user=follows.user)
            images += Image.objects.filter(user=follows.user)
            blog_posts += BlogPost.objects.filter(created_by=follows.user)
    else:
        user = None
        following_page = None
        profile = None

    video_comments = CommentsVideos.objects.all()

    all = list(posts) + list(videos) + list(images) + list(blog_posts)

    context = {'following': following,
               'posts': posts,
               'images': images,
               'videos': videos,
               'all': all,
               'blog_posts': blog_posts,
               'video_comments': video_comments,
               'profile': profile
               }
    return render(request, 'following.html', context)


# @login_required
# def mess(request):
# # used to add messages
# user = request.user
# messeges = Message.objects.all()
#
#
# if request.method == 'POST':
#     form = MessageForm(data=request.POST)
#     if form.is_valid():
#         messages = form.save(commit=False)
#         messages.sender = request.user
#         messages.save()
#         return HttpResponseRedirect(
#             reverse_lazy('person:messages'))
#     else:
#         print(form.errors)
# else:
#     form = MessageForm()
# context = {
#     'sent_message': sent_message,
#     'form': form,
#     'received_messages': received_messages,
#     'names':names
#
# }

# return render(request, 'message.html')

class CustomLogoutView(LogoutView, LoginRequiredMixin):
    template_name = 'logout.html'
    success_url = reverse_lazy('user:login')

    #
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'You have successfully logged out.'
        return context


class EditPost(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'
    success_url = reverse_lazy('user:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['prayer'] = Post.objects.get(pk=self.kwargs['pk'])
        return context


class EditImages(LoginRequiredMixin, UpdateView):
    model = Image
    form_class = ImageEditForm
    template_name = 'edit_image.html'
    success_url = reverse_lazy('user:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['image'] = Image.objects.get(pk=self.kwargs['pk'])
        return context


class EditVideo(LoginRequiredMixin, UpdateView):
    model = video
    form_class = VideoEditForm
    template_name = 'edit_video.html'
    success_url = reverse_lazy('user:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['video'] = video.objects.get(id=self.kwargs['pk'])
        return context


class DeletePosts(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('user:profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['post'] = Post.objects.get(id=self.kwargs['pk'])
        context['user'] = User.objects.get(id=self.request.user.id)
        return context


class DeleteVideo(LoginRequiredMixin, DeleteView):
    model = video
    template_name = 'delete_video.html'
    success_url = reverse_lazy('user:profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['video'] = video.objects.get(id=self.kwargs['pk'])
        context['user'] = User.objects.get(id=self.request.user.id)
        return context


class DeleteImage(LoginRequiredMixin, DeleteView):
    model = Image
    template_name = 'delete_img.html'
    success_url = reverse_lazy('user:profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['image'] = Image.objects.get(id=self.kwargs['pk'])
        context['user'] = User.objects.get(id=self.request.user.id)
        return context


def explore(request):
    user = request.user
    profile = request.user.profile
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'profile': profile,
        'user': user,

    }
    return render(request, 'explore.html', context)


class CreateBoard(LoginRequiredMixin, CreateView):
    model = Board
    form_class = BoardForm
    template_name = 'create_board.html'
    success_url = reverse_lazy('user:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteBoard(LoginRequiredMixin, DeleteView):
    model = Board
    template_name = 'deleteboard.html'
    success_url = reverse_lazy('user:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['board'] = Board.objects.get(pk=self.kwargs['pk'])
        return context


def boardview(request, username, board_id):
    board = get_object_or_404(Board, id=board_id)
    target_user =User.objects.get(username=username)
    if request.user.is_authenticated:
        profile = request.user.profile
        user_login = request.user
    else:
        profile = None
        user_login = None

        # Retrieve associated items in the specified order
      # Retrieve items with their order
    images = list(BoardImage.objects.filter(board=board).order_by('order'))
    videos = list(BoardVideo.objects.filter(board=board).order_by('order'))
    posts = list(BoardPost.objects.filter(board=board).order_by('order'))
    blogs = list(BoardBlogPost.objects.filter(board=board).order_by('order'))

    # Combine the sorted lists
    all_items = images + videos + posts + blogs

    # Define a function to get the order attribute based on the item type
    def get_order(item):
        if isinstance(item, BoardImage):
            return item.order
        elif isinstance(item, BoardVideo):
            return item.order
        elif isinstance(item, BoardPost):
            return item.order
        elif isinstance(item, BoardBlogPost):
            return item.order
        return 0

    # Sort the combined list by the order field
    all_items_sorted = sorted(all_items, key=lambda x: get_order(x))

    context = {'board': board,
               'profile': profile,
               'target_user': target_user,
               'videos': videos,
               'images': images,
               'posts': posts,
               'blogs': blogs,
               'items':all_items_sorted
               }
    return render(request, 'board.html', context)


class BlogPostCreate(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = CreateBlogForm
    template_name = 'createblogpost.html'
    success_url = reverse_lazy('user:profile')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)

        # Send real-time notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': f'{self.request.user} created a new blog post: {self.object.title}',
            }
        )
        for follower in self.request.user.following.all():
            notify.send(
                self.request.user,
                recipient=follower.user,
                verb='new Blog',
                description=f'{self.request.user} created a new blog post: {self.object.title}'
            )
        return response

        # Assign the current user to the created_by field

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context


def viewblogpost(request, pk, action_type):
    blog = BlogPost.objects.get(pk=pk)
    followerss = blog.created_by.profile.followers.all()
    if request.user.is_authenticated:
        user = request.user
        profile = request.user.profile
        boards = Board.objects.filter(user=request.user)
        if request.user not in blog.views.all():
            blog.views.add(request.user)

    else:
        user = None
        profile = None
        boards = []

    comment = CommentsBlog.objects.filter(blog=blog).order_by('date')

    # else:
    #     user=None
    #     profile =
    #     boards = None

    target_user = blog.created_by
    blog_posts = BlogPost.objects.filter(created_by=target_user)
    post = Post.objects.filter(user=target_user)
    vids = video.objects.filter(user=target_user)
    images = Image.objects.filter(user=target_user)
    alls = list(post) + list(vids) + list(images) + list(blog_posts)
    is_in_board = 'save to board'
    for board in boards:
        if blog in board.blogs.all():
            is_in_board = f' saved to {board.title}'
            break
        else:
            is_in_board = 'save to board'

    response_data = {}
    if request.user.is_authenticated:
        if action_type == 'like':
            blog = get_object_or_404(BlogPost, id=pk)

            if blog.likes.filter(id=request.user.id).exists():
                blog.likes.remove(request.user)
                response_data['liked'] = False
            else:
                blog.likes.add(request.user)
                response_data['liked'] = True
                notify.send(
                    request.user,
                    recipient=blog.created_by,
                    verb='post liked',
                    description='{} liked {}'.format(request.user, blog.title),
                )
            response_data['total_likes'] = post.likes.count()
        elif action_type == 'follow':
            if target_user.profile.followers.filter(id=request.user.id).exists():
                target_user.profile.followers.remove(request.user)
                response_data['follows'] = False
            else:
                target_user.profile.followers.add(request.user)
                response_data['follows'] = True
                notify.send(
                    request.user,
                    recipient=blog.created_by,
                    verb='new follower',
                    description=f'{request.user} followed you',
                )
            response_data['total_follows'] = target_user.profile.followers.count()

        elif action_type == 'save':
            blog = get_object_or_404(BlogPost, id=pk)
            if blog.saves.filter(id=request.user.id).exists():
                response_data['saved'] = True
            else:
                blog.saves.add(request.user)
                notify.send(
                    request.user,
                    recipient=blog.created_by,
                    verb='post saved',
                    description='{} saved {}'.format(request.user, blog.title),
                )
                response_data['saved'] = True
        elif Board.objects.filter(user=request.user, title=action_type).exists():
            board = get_object_or_404(Board, user=request.user, title=action_type)
            blog = get_object_or_404(BlogPost, pk=pk)
            if BoardBlogPost.objects.filter(board=board, blogpost=blog):
                response_data['saved'] = True
            else:
                next = board.get_next_order()
                BoardBlogPost.objects.create(board=board, blogpost=blog, order=next)
                notify.send(
                    request.user,
                    recipient=blog.created_by,
                    verb='post saved',
                    description='{} saved {} to board'.format(request.user, blog.title),
                )
                response_data['saved'] = True

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(response_data)
        elif (action_type == 'like' or action_type == 'follow' or action_type == 'save'
              or Board.objects.filter(
                    user=request.user, title=action_type).exists()):
            return redirect('person:viewpost',
                            kwargs={'pk': pk, 'created_by': post.created_by.pk, 'action_type': action_type})

    ws_url = f'ws://{request.get_host()}/ws/comment/{pk}/'
    blog = BlogPost.objects.get(pk=pk)

    all_blogs = blog_models.Post.objects.all()
    all_blog_posts = BlogPost.objects.all()
    similar_posts = find_similar_posts(blog.id)
    similar_blogposts = find_similar_blogposts_with_tags(blog.id)
    similar_blogs = find_similar_blogposts_to_post(blog, all_blogs)
    similar_images = find_similar_images_imgblog(blog.id)
    similar_videos = find_similar_videos_blogpost(blog)

    combined_results = []
    # Add images with similarity scores
    for img, score in similar_images:
        combined_results.append({'type': 'image', 'item': img, 'score': score})

    # Add videos with similarity scores
    for vid, score in similar_videos:
        combined_results.append({'type': 'video', 'item': vid, 'score': score})

    # Add prayers with similarity scores
    for prayer, score in similar_posts:
        combined_results.append({'type': 'prayer', 'item': prayer, 'score': score})

    # Add blog posts with similarity scores
    for blogpost, score in similar_blogposts:
        combined_results.append({'type': 'blogpost', 'item': blogpost, 'score': score})

    # Add blogs with similarity scores
    for blog, score in similar_blogs:
        combined_results.append({'type': 'blog', 'item': blog, 'score': score})

    # Sort combined results by similarity score in descending order
    sorted_results = sorted(combined_results, key=lambda x: x['score'], reverse=True)
    blog = BlogPost.objects.get(pk=pk)
    context = {'blog': blog,
               'profile': profile,
               'user': user,
               'target_user': target_user,
               'all_posts': post,
               'all_vids': vids,
               'all_images': images,
               # 'boards': boards,
               'items_by_date': alls,
               'is_in_board': is_in_board,
               'comment': comment,
               'ws_url': ws_url,
               'related_posts': sorted_results,
               'followers': followerss,
               # 'similar_images': similar_images,
               # 'similar_videos': similar_videos,
               # 'similar_blogs':similar_blogs

               }

    return render(request, 'viewblogpost.html', context)


@require_POST
def submit_blog_comment(request, id):
    if request.method == 'POST':
        form = CreateBlogCommentForm(data=request.POST)
        if form.is_valid():
            blog = get_object_or_404(BlogPost, id=id)
            comment = form.save(commit=False)
            comment.created_by = request.user
            comment.blog = blog
            comment.save()
            if blog:
                notify.send(
                    request.user,
                    recipient=blog.created_by,
                    verb='commented on your post',
                    description=comment.body,
                    # action_object=comment,
                    timestamp=timezone.now()
                )
            response_data = {
                'success': True,
                'comment': comment.body,
                'username': comment.created_by.username,
                'profile_picture': comment.created_by.profile.profile_picture.url,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'success': False, 'error': 'Form is not valid'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


class EditBlogPost(LoginRequiredMixin, UpdateView):
    model = BlogPost
    form_class = CreateBlogForm
    template_name = 'editblogpost.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['blog'] = BlogPost.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('person:viewblogpost', kwargs={'pk': self.object.pk, 'action_type': ' '})


class DeleteBlogPosts(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'deleteblog.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['blog'] = BlogPost.objects.get(id=self.kwargs['pk'])
        return context

    #
    def get_success_url(self):
        return reverse_lazy('person:follow_unfollow_user',
                            kwargs={'username': self.object.created_by.username, 'action_type': ' '})

    #
    #


from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Comments


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comments
    template_name = 'deletecomment.html'

    def get_success_url(self):
        comment = Comments.objects.get(pk=self.kwargs['pk'])
        # Ensure the correct parameters are being passed to reverse_lazy
        return reverse_lazy('person:viewpost', kwargs={
            'pk': comment.user.id,  # Assuming pk should refer to the post ID
            'post_id': comment.post.id,
            'action_type': ' ',
            # Assuming post_id refers to the post ID
        })

    def get(self, request, *args, **kwargs):
        # Override get method to call post for direct deletion without confirmation template
        return self.post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        comment = Comments.objects.get(pk=self.kwargs['pk'])
        context = super().get_context_data()
        context['comment'] = Comments.objects.get(pk=self.kwargs['pk'])
        # context['post']=Post.objects.get(pk=comment.post.id)
        return context


class CommentDeleteViewBlog(LoginRequiredMixin, DeleteView):
    model = CommentsBlog
    template_name = 'deletecommentblog.html'

    def get_success_url(self):
        comment = CommentsBlog.objects.get(pk=self.kwargs['pk'])
        # Ensure the correct parameters are being passed to reverse_lazy
        return reverse_lazy('person:viewblogpost', kwargs={
            # Assuming pk should refer to the post ID
            'pk': comment.blog.id,
            'action_type': ' ',
            # Assuming post_id refers to the post ID
        })

    def get(self, request, *args, **kwargs):
        # Override get method to call post for direct deletion without confirmation template
        return self.post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        comment = CommentsBlog.objects.get(pk=self.kwargs['pk'])
        context = super().get_context_data()
        context['comment'] = CommentsBlog.objects.get(pk=self.kwargs['pk'])
        # context['post']=Post.objects.get(pk=comment.post.id)
        return context


class CommentDeleteViewVideo(LoginRequiredMixin, DeleteView):
    model = CommentsVideos
    template_name = 'deletecommentvideo.html'

    def get_success_url(self):
        comment = CommentsVideos.objects.get(pk=self.kwargs['pk'])
        # Ensure the correct parameters are being passed to reverse_lazy
        return reverse_lazy('person:viewvideo', kwargs={
            # Assuming pk should refer to the post ID
            'pk': comment.user.id,
            'action_type': ' ',
            'video_id': comment.video.id
            # Assuming post_id refers to the post ID
        })

    def get(self, request, *args, **kwargs):
        # Override get method to call post for direct deletion without confirmation template
        return self.post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        comment = CommentsVideos.objects.get(pk=self.kwargs['pk'])
        context = super().get_context_data()
        context['comment'] = CommentsVideos.objects.get(pk=self.kwargs['pk'])
        # context['post']=Post.objects.get(pk=comment.post.id)
        return context


class CommentDeleteImage(LoginRequiredMixin, DeleteView):
    model = CommentsImage
    template_name = 'deletecommentimage.html'

    def get_success_url(self):
        comment = CommentsImage.objects.get(pk=self.kwargs['pk'])
        # Ensure the correct parameters are being passed to reverse_lazy
        return reverse_lazy('person:viewimage', kwargs={
            # Assuming pk should refer to the post ID
            'pk': comment.user.id,
            'action_type': ' ',
            'image_id': comment.image.id
            # Assuming post_id refers to the post ID
        })

    def get(self, request, *args, **kwargs):
        # Override get method to call post for direct deletion without confirmation template
        return self.post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        comment = CommentsImage.objects.get(pk=self.kwargs['pk'])
        context = super().get_context_data()
        context['comment'] = CommentsImage.objects.get(pk=self.kwargs['pk'])
        # context['post']=Post.objects.get(pk=comment.post.id)
        return context


#

@login_required
def view_board(request, board_id):
    board = get_object_or_404(Board, id=board_id, user=request.user)

    # Fetching all related items with their order
    images = BoardImage.objects.filter(board=board).select_related('image')
    videos = BoardVideo.objects.filter(board=board).select_related('video')
    posts = BoardPost.objects.filter(board=board).select_related('post')
    blogs = BoardBlogPost.objects.filter(board=board).select_related('blog')

    # Combine all items into a list with type identifier
    combined_items = [
                         {'type': 'image', 'id': item.id, 'order': item.order, 'obj': item.image} for item in images
                     ] + [
                         {'type': 'video', 'id': item.id, 'order': item.order, 'obj': item.video} for item in videos
                     ] + [
                         {'type': 'post', 'id': item.id, 'order': item.order, 'obj': item.post} for item in posts
                     ] + [
                         {'type': 'blog', 'id': item.id, 'order': item.order, 'obj': item.blog} for item in blogs
                     ]

    # Sort combined items by order
    combined_items.sort(key=lambda x: x['order'])

    context = {
        'board': board,
        'items': combined_items,
    }
    return render(request, 'edit_board.html', context)


import logging

logger = logging.getLogger(__name__)


@login_required
@csrf_exempt
def reorder_items(request, board_id):
    if request.method == 'POST':
        board = get_object_or_404(Board, id=board_id, user=request.user)

        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            item_order = body_data.get('item_order')

            if not item_order:
                return JsonResponse({'error': 'No item order provided'}, status=400)

            for index, item_identifier in enumerate(item_order):
                item_type, item_id = item_identifier.split('-')

                if item_type == 'image':
                    image = get_object_or_404(BoardImage, id=item_id, board=board)
                    image.order = index
                    image.save()
                elif item_type == 'video':
                    video = get_object_or_404(BoardVideo, id=item_id, board=board)
                    video.order = index
                    video.save()
                elif item_type == 'post':
                    post = get_object_or_404(BoardPost, id=item_id, board=board)
                    post.order = index
                    post.save()
                elif item_type == 'blog':
                    blog = get_object_or_404(BoardBlogPost, id=item_id, board=board)
                    blog.order = index
                    blog.save()

            return JsonResponse({'status': 'success'})

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            logger.error(f"Error updating order: {e}")
            return JsonResponse({'error': 'An error occurred'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)