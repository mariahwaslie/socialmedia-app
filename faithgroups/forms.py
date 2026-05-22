from django import forms
from .models import *
from person.models import BlogPost, Post, Image, video as Video
# from datetimepicker.widgets import DateTimePicker
from location_field.forms.plain import PlainLocationField

class GroupCreationRequestForm(forms.ModelForm):
    class Meta:
        model = GroupCreationRequest
        fields = ['group_name', 'description', 'privacy', 'join_privacy', 'who_can_post']

class ChurchCreationRequestForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, label='Create an in detail description of what '
                                                               'your church believes, your values, '
                                                               'mission statement, and anything else that '
                                                               'may be relevant')
    class Meta:
        model = ChurchCreationRequest
        fields = ['group_name', 'description', 'privacy', 'join_privacy', 'who_can_post']


class ApproveGroupCreation(forms.Form):
    confirm_approval = forms.BooleanField(
        label="Approve Group Creation",
        initial=True,
        required=True
    )
    # Optionally, add a comment field for admin notes
    admin_comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Admin Comment"
    )


class GroupRequestForm(forms.ModelForm):
    class Meta:
        model = GroupRequest
        fields = ['text']


class GroupPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'tags']

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super(GroupPostForm, self).__init__(*args, **kwargs)
        if group:
            self.instance.group = group
            # self.fields['group'].widget = forms.HiddenInput()
            # if group.privacy == 'private':
            #     self.fields['privacy'].widget = forms.HiddenInput()
            #     self.fields['privacy'].inital = 'public'
            # elif group.privacy == 'public':
            #     self.fields['privacy'].choices = [
            #         ('public', 'private'),
            #         ('Public', 'Private')]
            #
# forms.py
class GroupPrayerForm(forms.ModelForm):
    class Meta:
        model =Post
        fields = ['title', 'content', 'tags','category']
    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super(GroupPrayerForm, self).__init__(*args, **kwargs)
        if group:
            self.instance.group = group

class GroupVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title','description', 'video_file', 'tags', 'category']
    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super(GroupVideoForm, self).__init__(*args, **kwargs)
        if group:
            self.instance.group = group


class GroupImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title','description', 'image', 'tags_img']
    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super(GroupImageForm, self).__init__(*args, **kwargs)
        if group:
            self.instance.group = group
class LocationForm(forms.Form):
    latitude = forms.FloatField()
    longitude = forms.FloatField()
class EventForm(forms.ModelForm):
    event_date= forms.DateTimeField(widget=forms.DateInput(attrs={'type':'datetime-local'}))
    # registration_deadline= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'event_date',
            'event_type',
            # 'location_type',
            'organizer',
            # 'location_details',

            # 'max_attendees',

            # 'registration_required',
            # 'registration_deadline',
            # 'cost',
            # 'duration',
            # 'is_recurring',
            # 'recurrence_pattern',
            # 'accessibility_options',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form fields here if needed
        # self.fields['location_details'].required = False
        # self.fields['accessibility_options'].required = False

