#
#
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from tinymce.widgets import TinyMCE
# from django.contrib.flatpages.models import FlatPage
# from user.models import *
# from django import forms
# from allauth.account.forms import SignupForm
#
# class GoogleSignUpForm(SignupForm):
#     first_name = forms.CharField(label='First Name', max_length=50)
#     last_name = forms.CharField(label='Last Name', max_length=50)
#     username = forms.CharField(label='Username', max_length=50)
#     email = forms.CharField(label='Email', max_length=50)
#     # password = forms.CharField(label='Password', widget=forms.PasswordInput)
#     # password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
#     def form_valid(self, request):
#         user = super().save(request)
#         first_name = self.cleaned_data['first_name']
#         last_name = self.cleaned_data['last_name']
#         email = self.cleaned_data['email']
#         username=self.cleaned_data['username']
#         password = self.cleaned_data['password']
#
#         Profile.objects.create(user=user)
#         Follow.objects.create(follower=user)
#         return user
#
#
#
#
