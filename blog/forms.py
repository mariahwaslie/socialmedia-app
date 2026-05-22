from django import forms
from .models import Post
from tinymce.widgets import TinyMCE
from django.contrib.flatpages.models import FlatPage


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class PostForm(forms.ModelForm):

    content = forms.CharField(
        widget=TinyMCE(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    class Meta:
        model = Post
        fields = ['title', 'content']

