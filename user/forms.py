from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from tinymce.widgets import TinyMCE
from django.contrib.flatpages.models import FlatPage
from .models import *
from django import forms

class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture')


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

