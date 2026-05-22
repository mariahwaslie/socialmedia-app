
from django import forms
from .models import Playlist, PlaylistItem, video

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title', 'description','tags','privacy']

class PlaylistItemForm(forms.ModelForm):
    class Meta:
        model = PlaylistItem
        fields = ['video']  # Use video field instead of URL
    video = forms.ModelChoiceField(queryset=video.objects.all(),
                                   empty_label="Select a video")
