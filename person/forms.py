from django import forms
from person.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from tinymce.widgets import TinyMCE
from django.contrib.flatpages.models import FlatPage

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ['title', 'content', 'category','tags','privacy']


class VideoForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = video
        fields = ('title', 'description', 'video_file', 'category','tags','privacy')
        # widgets={
        #     'video-file': forms.ClearableFileInput(attrs={'multiple': False,
        #                                                   'id':'video-file',
        #                                                   'type':'file',
        #                                                   'accept':'video/*'
        #                                                   }),
        #
        # }
# # class TikTokAccountForm(forms.ModelForm):
# #     url_username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
# #     class Meta:
# #         model=video
# #         fields ='url_username'
#




class PodcastForm(forms.ModelForm):
    class Meta:
        model=Podcast
        fields= ('title', 'description', 'audio_file', 'picture','is_public')
class ImageForm(forms.ModelForm):
    tags_img = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    class Meta:
        model=Image

        fields= ('title', 'description', 'image','privacy','tags_img')
class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('body',)
class CommentImageForm(forms.ModelForm):
    class Meta:
        model=CommentsImage
        fields=('body',)

class CommentsVideoForm(forms.ModelForm):
    class Meta:
        model=CommentsVideos
        widgets ={
            'parent': forms.HiddenInput(),
        }
        fields=('body','parent')

# class MessageForm(forms.ModelForm):
#     class Meta:
#         model=Message
#         fields= ('body', 'receiver')
class ImageEditForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=('title', 'description','privacy','tags_img','privacy')
class VideoEditForm(forms.ModelForm):
    class Meta:
        model=video
        fields=('title', 'description','category', 'tags','privacy')



class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class CreateBlogForm(forms.ModelForm):

    content = forms.CharField(
        widget=TinyMCE(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    class Meta:
        model = BlogPost
        fields = ['title', 'content','privacy']
class CreateBlogCommentForm(forms.ModelForm):
    class Meta:
        model= CommentsBlog
        fields = ['body']

class BoardForm(forms.ModelForm):
    class Meta:
        model=Board
        fields=('title', 'description', 'privacy')
class EditBoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'description', 'privacy', 'images', 'videos', 'posts', 'blogs']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'images': forms.CheckboxSelectMultiple(),
            'videos': forms.CheckboxSelectMultiple(),
            'posts': forms.CheckboxSelectMultiple(),
            'blogs': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user from kwargs
        super(EditBoardForm, self).__init__(*args, **kwargs)
        if user:
            # Filter related fields to show only items related to the user
            self.fields['images'].queryset = Image.objects.filter(user=user)
            self.fields['videos'].queryset = video.objects.filter(user=user)
            self.fields['posts'].queryset = Post.objects.filter(user=user)
            self.fields['blogs'].queryset = BlogPost.objects.filter(created_by=user)
