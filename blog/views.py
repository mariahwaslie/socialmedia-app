from django.shortcuts import render, redirect
from .models import *
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from user.models import Profile




# Create your views here.
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=request.user)
    else:
        profile = None
        user = None


    context = {'posts': posts,
               'user': user,
               'profile': profile}
    return render(request, 'bloglist.html', context)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'createblog.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        # profile = Profile.objects.get(user=self.request.user)
        form.instance.created_by = self.request.user
        # Assign the current user to the created_by field
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        context['profile'] = Profile.objects.get(user=user)
        return context

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        user= request.user
    else:
        profile = None
        user = None
    context = {'post': post,
               'profile': profile,
               'user': user}
    return render(request, 'blogpost.html', context)

class EditBlog(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'editblog.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['blog']=Post.objects.get(pk=self.kwargs['pk'])
        return context
    def get_success_url(self):
        return reverse_lazy('person:viewblogpost', kwargs={'pk': self.object.pk,'action_type': ' '})


class DeleteBlog(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'deleteblog.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)
    def get_context_data(self, **kwargs):
        context= super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['blog']=Post.objects.get(id=self.kwargs['pk'])
        return context
    #
    def get_success_url(self):
        return reverse_lazy('person:follow_unfollow_user', kwargs={'username': self.object.created_by.username, 'action_type': ' '})

    #
    #

