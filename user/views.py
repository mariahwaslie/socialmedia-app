from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
import user
from .forms import *
from .models import *
from person.models import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
#
class indexView(TemplateView):
    template_name = 'index.html'

# def register(request):
#     registered = False
#
#     if request.method == 'POST':
#
#         user_form = UserForm(data=request.POST)
#         if user_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             Profile.objects.create(user=user)
#             Follow.objects.create(user=user)
#             user.save()
#             # Registration Successful!
#             registered = True
#             return HttpResponseRedirect(reverse('person:profile'))
#
#         else:
#             # One of the forms was invalid if this else gets called.
#             print(user_form.errors)
#
#     else:
#         user_form = UserForm()
#
#     # This is the render and context dictionary to feed
#     # back to the registration.html file page.
#     return render(request, 'sign_up.html',
#                   {'user_form': user_form,
#                    'registered': registered})
class SignUpView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        Follow.objects.create(follower=user)
        return super().form_valid(form)



def user_login(request):
    if request.method == 'POST':
        # First get the username and password supplied
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    return redirect(reverse('person:follow_unfollow_user',
                                        kwargs={'username': username,
                                                    'action_type': ' ' }
                                            ))
                else:
                    # If account is not active:
                    messages.error(request, 'Your account is disabled.')
            else:
                messages.error(request, "Invalid login details.")
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()

            # Nothing has been provided for username or password.
    return render(request, 'login.html', {'form': form })

class UpdateProfile(CreateView, LoginRequiredMixin):
        model = Profile
        form_class = UserProfileForm
        template_name = 'update_profile.html'
        success_url = reverse_lazy('user:profile')

        def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)

class updateUser(UpdateView, LoginRequiredMixin):
        model = User
        form_class = UpdateUserForm
        template_name = 'update_user.html'
        success_url = reverse_lazy('user:profile')


class UpdateProfile(CreateView, LoginRequiredMixin):
    model = Profile
    form_class = UserProfileForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('user:profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class updateUser(UpdateView, LoginRequiredMixin):
    model = User
    form_class = UpdateUserForm
    template_name = 'update_user.html'
    success_url = reverse_lazy('user:profile')


class ProfileView(TemplateView, LoginRequiredMixin):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['user_about'] = Profile.objects.filter(user=self.request.user).values('bio', 'profile_picture').first()

        return context



class ViewImages(TemplateView, LoginRequiredMixin):
    template_name = 'profileimageview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Image.objects.filter(user=self.request.user).values('title', 'image', 'description', 'created_at',
                                                                     'id')
        images_sorted = sorted(
            list(images),
            key=lambda k: k['created_at'],
            reverse=True
        )

        context['images_sorted'] = images_sorted
        context['user_about'] = Profile.objects.filter(user=self.request.user).values('bio', 'profile_picture').first()
        context['profile']= Profile.objects.get(user=self.request.user)

        return context


class ViewHistory(TemplateView, LoginRequiredMixin):
    template_name = 'history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs =BlogPost.objects.filter(views=self.request.user).values('title', 'created_at', 'id','content','created_by')
        images = Image.objects.filter(views=self.request.user).values('title', 'image', 'created_at', 'id', 'user')
        posts = Post.objects.filter(views=self.request.user).values('title', 'content', 'created_at', 'id', 'user')
        videos = video.objects.filter(views=self.request.user).values('title', 'video_file', 'created_at', 'id', 'user')
        history = list(posts) + list(videos) + list(images) + list(blogs)
        history_sorted = sorted(
            list(history),
            key=lambda k: k['created_at'],
            reverse=True
        )
        context['history'] = history
        context['history_sorted'] = history_sorted
        context['videos'] = videos
        context['posts'] = posts
        context['images'] = images
        context['blogs'] =blogs
        context['profile']= Profile.objects.get(user=self.request.user)
        return context


class ViewPosts(TemplateView, LoginRequiredMixin):
    template_name = 'userpost.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.filter(user=self.request.user).values('title', 'content', 'created_at',
                                                                  'category', 'id')
        timeline_items = sorted(
            list(post),
            key=lambda k: k['created_at'],
            reverse=True
        )

        context['timeline_items'] = timeline_items
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['user_about'] = Profile.objects.filter(user=self.request.user).values('bio', 'profile_picture').first()

        return context

class ViewBlogs(TemplateView, LoginRequiredMixin):
    template_name = 'viewblogsprofile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = BlogPost.objects.filter(created_by=self.request.user).values('title', 'content', 'created_at',
                                                                  'created_by', 'id')
        timeline_items = sorted(
            list(blogs),
            key=lambda k: k['created_at'],
            reverse=True
        )

        context['timeline_items'] = timeline_items
        context['user_about'] = Profile.objects.filter(user=self.request.user).values('bio', 'profile_picture').first()
        context['blogs']=BlogPost.objects.filter(created_by=self.request.user).values('title', 'content', 'created_at',
                                                                  'created_by', 'id')
        return context

class ViewVideos(LoginRequiredMixin, TemplateView):
    template_name = 'profilevideos.html'
    success_url = reverse_lazy('person:myvids')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = video.objects.filter(user=self.request.user).values('title', 'description', 'created_at',
                                                                                'video_file', 'category', 'id')
        context['user_about'] = Profile.objects.filter(user=self.request.user).values('bio', 'profile_picture').first()
        context['profile']= Profile.objects.get(user=self.request.user)


        return context
