from django import forms
from .models import  Message,ChatRoom,SingleChat
from tinymce.widgets import TinyMCE
from django.contrib.flatpages.models import FlatPage


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
class ChatForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name', 'description','participants' ]
# class ChatRoomEditForm(forms.ModelForm):
#     class Meta:
#         model = ChatRoom
#         fields = ['name', 'description', 'participants' ]